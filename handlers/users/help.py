from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    await message.answer(
        "Bu bot Freelansing (yollanma ish topish) uchun yaratilgan siz buyerda online ish topishingiz mumkin misol "
        "uchun uy-joy chizmalari, web, android dasturlar vahokozolarga buyurtma bersihingiz mukin buyurtma berish tekin"
        " ammo ish haqqini ish ni bajaruvchi freelanser(yollanma ishchi) bilan kelishasiz")
