import asyncio
from loader import dp, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.state import WorkInfo
from keyboards.inline.main import confirm, salary
from keyboards.default.main import main, work_keyboard, phone, skip

summa = ""
user_id = 5248186563


@dp.message_handler(text="💻 Ish (topish) bo'yicha", state="*")
async def freelance(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    await asyncio.sleep(0.05)
    await message.answer("O'zingizga kerakli bo'limni tanlang 👇", reply_markup=work_keyboard)


@dp.message_handler(
    text=["👥 Sherik kerak", "🏭 Ish joyi kerak", "🎓 Shogirt kerak", "🧑‍💻 Xodim kerak", "👨‍🏫 Ustoz kerak"], state="*")
async def freelance(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    await asyncio.sleep(0.05)
    await message.answer("Ismingizni to'liq kiriting\n\nMisol: <b>Soliyev Anvar</b>",
                         reply_markup=ReplyKeyboardRemove())

    await WorkInfo.fullname.set()


@dp.message_handler(state=WorkInfo.fullname)
async def freelance(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data({"fullname": fullname})
    await message.answer("Yoshingizni kiriting\n\nMisol: <b>18</b>")
    await WorkInfo.next()


@dp.message_handler(lambda message: message.text.isdigit(), state=WorkInfo.age)
async def freelance(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data({"age": age})
    await message.answer("Dasturlashda ishlatiladigan tilingizni kiriting\nDizayner yoki shunga o'xshash bo'lsangiz "
                         "siz ishlaydigan dastur nomini\n\nMisol: <b>Python</b> yoki <b>3dMax</b>")
    await WorkInfo.next()


@dp.message_handler(state=WorkInfo.language)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"language": message.text})
    await message.answer("Pastdagi tugma orqali raqamingizni yuboring 👇", reply_markup=phone)
    await WorkInfo.next()


@dp.message_handler(content_types=['contact'], state=WorkInfo.phone)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer("Manzilingizni to'liq kiriting\n\nMisol: <b>O'zbekiston Xorazm Urganch</b>",
                         reply_markup=ReplyKeyboardRemove())
    await WorkInfo.next()


@dp.message_handler(state=WorkInfo.location)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"location": message.text})
    await message.answer(
        "Hozirda qayerda ishlashingiz yoki o'qishingizni yozing\n\nMisol: <b>Figma</b> yoki <b>TATU</b>")
    await WorkInfo.next()


@dp.message_handler(state=WorkInfo.position)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"position": message.text})
    await message.answer("Ishlay oladigan vatingizni kiriting\n\nMisol: \"08:00 20:00\" yoki 24/7")
    await WorkInfo.next()


@dp.message_handler(state=WorkInfo.work_time)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"work_time": message.text})
    await message.answer(
        "Tajribangizni yilda kiriting\nDiqqat bu ma'lumot faqat yilda hisoblanadi\n\nMisol: <b>1</b> yoki <b>0.5+</b>")
    await WorkInfo.next()


@dp.message_handler(state=WorkInfo.experience)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"experience": message.text})
    await message.answer(
        "Ish uchun qancha ish haqqi to'laysiz ?\nYoki qancha pulga ishlamoqchisiz ?\nUshbu tugmalar orqali yozing. "
        "Summa nolligi ( 0 ) xizmat tekin ekanligini anglatadi!\nSumma dollarda ($) hisoblanadi \n\nMisol: <b>2000</b>",
        reply_markup=salary)
    await WorkInfo.next()


@dp.callback_query_handler(text="done", state='*')
async def callme(call: types.CallbackQuery, state: FSMContext):
    global summa
    for i in range(len(summa)):
        if summa.startswith("0") or summa.startswith(" "):
            summa = summa[1:]
    if summa == "":
        summa = "tekin"
    await state.update_data({"salary": summa})
    await call.message.edit_text(f"Bajarildi!\nSumma saqlandi\nSumma {summa} $", reply_markup=None)
    await call.message.answer("Agar qo'shimcha ma'lumot bo'lsa yozing aks holda tashlab ketishni bosing",
                              reply_markup=skip)
    summa = ""
    await WorkInfo.next()


@dp.callback_query_handler(text="clear", state='*')
async def callme(call: types.CallbackQuery):
    global summa
    summa = "0"
    await call.message.edit_text(f"Joriy kiritmoqchi bo'lgan summangiz: <b>{summa} $</b>", reply_markup=salary)
    summa = ""


@dp.callback_query_handler(text="yes", state='*', chat_id=ADMINS)
async def callme(call: types.CallbackQuery):
    global user_id
    await call.message.edit_reply_markup(None)
    message_id = await bot.send_message(chat_id="@silkanomi2", text=call.message.html_text)
    await bot.send_message(chat_id=user_id,
                           text=f"Sizning e'loningiz @silkanomi2 kanaliga joylandi\n[Xabarni "
                                f"ko'rish](https://t.me/silkanomi2/{message_id['message_id']})",
                           parse_mode="markdown", disable_web_page_preview=True)
    await call.message.edit_text(call.message.text, reply_markup=None)


@dp.callback_query_handler(text="no", state='*', chat_id=ADMINS)
async def callme(call: types.CallbackQuery):
    global user_id
    await call.message.edit_text(call.message.text, reply_markup=None)
    await bot.send_message(chat_id=user_id,
                           text="Hurmatli foydalanuvchi siz yuborgan xabar(e'lon)da adminlarimiz ga nomaqbul kelgan "
                                "kontent topildi shu tufayli xabar(e'lon)ingizni qayta ko'rib chiqib, yuborishingizni "
                                "so'raymiz! \n\nHurmat bilan UzBCoder_bot", reply_markup=None)


@dp.callback_query_handler(text="yes", state='*')
async def callme(call: types.CallbackQuery):
    await call.message.send_copy(chat_id=5248186563, reply_markup=confirm)
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main)


@dp.callback_query_handler(text="no", state='*')
async def callme(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main)


@dp.callback_query_handler(state='*')
async def callme(call: types.CallbackQuery):
    global summa
    summa += call.data
    await call.message.edit_text(f"Joriy kiritmoqchi bo'lgan summangiz: <b>{summa} $</b>", reply_markup=salary)


@dp.message_handler(state=WorkInfo.description)
async def freelance(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    if message.text == "➡️ Tashlab ketish":
        data = await state.get_data()
        fin = f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Hozirda: <b>{data.get('position')} da ishlaydi (yoki o'qiydi)</b>\n" \
              f"Ish vaqti: <b>{data.get('work_time')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n" \
              f"Ish haqi: <b>{data.get('salary')} $</b>"
        await message.answer(fin, reply_markup=confirm)
        await state.finish()
    else:
        await state.update_data({"description": message.text})
        data = await state.get_data()
        fin = f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Hozirda: <b>{data.get('position')} da ishlaydi (yoki o'qiydi)</b>\n" \
              f"Ish vaqti: <b>{data.get('work_time')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n" \
              f"Ish haqi: <b>{data.get('salary')} $</b>\n" \
              f"Qo'shimcha ma'lumot: <i>{data.get('description')}</i>"
        await message.answer(fin, reply_markup=confirm)
        await state.finish()
