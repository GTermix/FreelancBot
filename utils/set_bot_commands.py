from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni (qayta) ishga tushurish"),
            types.BotCommand("admin", "Adminga xabar yuborish"),
            types.BotCommand("help", "Botni ishlatish uchun yordam (qo'llanma)"),
        ]
    )
