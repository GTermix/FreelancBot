from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def check_subs(links):
    check_button = InlineKeyboardMarkup(row_width=1)
    for link in links:
        check_button.add(InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=link))

    check_button.add(InlineKeyboardButton(text="✔️ Obunani tekshirish", callback_data="check_subs"))
    return check_button
