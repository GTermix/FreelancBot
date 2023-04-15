from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton("✅ Ha", callback_data="yes"), InlineKeyboardButton("❎ Yo'q", callback_data="no"))


def confirm_admin(user_id):
    confirmation_admin = InlineKeyboardMarkup()
    confirmation_admin.add(InlineKeyboardButton("✅ Ha", callback_data=f"yes_{user_id}"),
                           InlineKeyboardButton("❎ Yo'q", callback_data=f"no_{user_id}"))
    return confirmation_admin


def contact_admin(user_id, msg_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Javob yozish", callback_data=f"reply_{user_id}_{msg_id}"))
    keyboard.add(InlineKeyboardButton("O'qilgan deb belgilash",callback_data="read"))
    return keyboard


salary = InlineKeyboardMarkup()
for i in range(1, 10):
    salary.insert(InlineKeyboardButton(str(i), callback_data=str(i)))
salary.add(InlineKeyboardButton("0", callback_data="0"))
salary.row(InlineKeyboardButton("🗑 Summani tozalash", callback_data="clear"),
           InlineKeyboardButton("✅ Bajarildi", callback_data='done'))
