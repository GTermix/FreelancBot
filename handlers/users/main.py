from loader import dp, bot
from data.config import ADMINS, CHANNELS
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.state import *
from utils.misc.subscription import check as subscription_check
from keyboards.default.main import main_markup, work_keyboard
from keyboards.inline.main import contact_admin

user_id = ADMINS[0]


@dp.message_handler(text="💻 Ish (topish) bo'yicha", state=MainState.command)
async def freelance(message: types.Message, state: FSMContext):
    await message.answer("O'zingizga kerakli bo'limni tanlang 👇", reply_markup=work_keyboard)
    await MainState.next()


@dp.message_handler(state=MainState.end)
async def freelance(message: types.Message):
    msg = message.text
    if msg == "👥 Sherik kerak":
        await message.answer("Ismingizni to'liq kiriting\n\nMisol: <b>Soliyev Anvar</b>",
                             reply_markup=ReplyKeyboardRemove())
        await PartnerInfo.name.set()
    elif msg == "🏭 Ish joyi kerak":
        await message.answer("Ismingizni to'liq kiriting\n\nMisol: <b>Soliyev Anvar</b>",
                             reply_markup=ReplyKeyboardRemove())
        await WorkplaceInfo.name.set()
    elif msg == "🧑‍💻 Xodim kerak":
        await message.answer(
            "Ish joyi(kompaniya, korparatsiya)nomi kiritng\n\nMisol: <b>Fincube</b> yoki <b>Mindbook</b>",
            reply_markup=ReplyKeyboardRemove())
        await EmployeeInfo.name.set()
    else:
        await message.answer("Menga tugmalar orqali xabar yuboring")


@dp.callback_query_handler(text="check_subs", state='*')
async def subs_check(call: types.CallbackQuery):
    channels_format = list()
    result = True
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format.append(invite_link)
        result *= await subscription_check(user_id=call.from_user.id,
                                           channel=channel)
    if not result:
        await call.answer("Hamma kanallarga a'zo bo'ling")
    else:
        await call.message.delete()
        msg = f"Assalomu alaykum, xush kelibsiz\n👤 <b><a href=\"tg://user?id={call.from_user.id}\">" \
              f"{call.from_user.full_name}</a></b>!" \
              f"\nBotimizdan foydalanishingiz mumkin. Tugmalardan foydalanib menga xabar yuboring 🔽"
        await call.message.answer(msg, reply_markup=main_markup)


@dp.callback_query_handler(lambda call: call.data[:4] in ["repl", "read"], state='*', chat_id=ADMINS)
async def reply_user_request(call: types.CallbackQuery, state: FSMContext):
    if call.data == "read":
        await call.message.edit_reply_markup()
    else:
        data_ = call.data.split('_')
        await state.update_data({"user_id": data_[1], "msg_id": data_[2]})
        await call.message.answer("Yubormoqchi bo'lgan xabaringizni yuboring")
        await ReplyUser.send.set()


@dp.message_handler(content_types=['any'], state=ReplyUser.send)
async def reply_message_to_user(message: types.Message, state: FSMContext):
    data_ = await state.get_data()
    await bot.copy_message(data_.get('user_id'), message.from_user.id, message.message_id,
                           reply_to_message_id=data_.get('msg_id'))
    await message.answer("Xabaringiz foydalanuvchiga muvoffaqiyatli yetkazildi", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.callback_query_handler(lambda call: call.data[:3] in ["yes", "no_"], state='*', chat_id=ADMINS)
async def callme(call: types.CallbackQuery):
    data_ = call.data.split('_')
    if data_[0] == "yes":
        message_id = await bot.send_message(chat_id="@FreelanceUz_channel", text=call.message.html_text)
        await bot.send_message(chat_id=data_[1],
                               text=f"Sizning e'loningiz @FreelanceUz_channel kanaliga joylandi\n[Xabarni "
                                    f"ko'rish](https://t.me/FreelanceUz_channel/{message_id['message_id']})",
                               parse_mode="markdown", disable_web_page_preview=True)
        await call.message.edit_text(call.message.text, reply_markup=None)
    elif data_[0] == "no":
        await call.message.edit_text(call.message.text, reply_markup=None)
        await bot.send_message(chat_id=data_[1],
                               text="Hurmatli foydalanuvchi siz yuborgan xabar(e'lon)da adminlarimiz ga nomaqbul kelgan "
                                    "kontent topildi shu tufayli xabar(e'lon)ingizni qayta ko'rib chiqib, yuborishingizni "
                                    "so'raymiz! \n\nHurmat bilan bot admini", reply_markup=None)


@dp.message_handler(commands=['admin'], state='*')
async def contact(message: types.Message):
    await message.answer("Menga adminga yubormoqchi bo'lgan xabar(fayl)ingizni yuboring men uni adminga yetkazaman")
    await ContactAdmin.mesg.set()


@dp.message_handler(content_types=['any'], state=ContactAdmin.mesg)
async def contact(message: types.Message, state: FSMContext):
    await bot.copy_message(chat_id=ADMINS[0], from_chat_id=message.from_user.id,caption="kahsbcu", message_id=message.message_id,
                           reply_markup=contact_admin(message.from_user.id, message.message_id))
    await message.answer("Xabaringiz adminga yetkazildi. Xabaringiz bo'yicha siz bilan bog'lanishadi")
    await message.answer("Bosh menydasiz kerakli bo'limni tanlang", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.message_handler(text="🚪 Bosh menu", state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer("Bosh menyudasiz kerakli bo'imni tanlang", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()
