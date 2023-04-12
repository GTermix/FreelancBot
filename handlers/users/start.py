from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from loader import dp, db, bot
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from keyboards.default.main import main_markup
from states.state import MainState
from utils.misc.subscription import check as subscription_check
from data.config import CHANNELS
from keyboards.inline.subscription import check_subs


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    channels_format = list()
    result = True
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format.append(invite_link)
        result *= await subscription_check(user_id=message.from_user.id,
                                           channel=channel)
    if not result:
        await message.answer(f"Quyidagi kanallarga obuna bo'ling 👇",
                             reply_markup=check_subs(channels_format))
    else:
        msg = f"Assalomu alaykum, xush kelibsiz\n👤 <b><a href=\"tg://user?id={message.from_user.id}\">" \
              f"{message.from_user.full_name}</a></b>!" \
              f"\nBotimizdan foydalanishingiz mumkin. Tugmalardan foydalanib menga xabar yuboring 🔽"
        await message.answer(msg, reply_markup=main_markup)
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    name = message.from_user.username
    await bot.send_message(chat_id=ADMINS[0], text=f"@{name} botga qo'shildi")
    await MainState.command.set()
