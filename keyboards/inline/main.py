from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


salary = InlineKeyboardMarkup()
for i in range(1, 10):
    salary.insert(InlineKeyboardButton(str(i), callback_data=str(i)))
salary.add(InlineKeyboardButton("0", callback_data="0"))
salary.row(InlineKeyboardButton("🗑 Summani tozalash", callback_data="clear"),
           InlineKeyboardButton("✅ Bajarildi", callback_data='done'))

