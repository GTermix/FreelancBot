from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_markup.add(KeyboardButton("⚡️ Tezkor buyurtmalar (Freelance)"),
         KeyboardButton("💻 Ish (topish) bo'yicha"))

work_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("👥 Sherik kerak"), KeyboardButton("🏭 Ish joyi kerak")],
    [KeyboardButton("🧑‍💻 Xodim kerak"), KeyboardButton("👨‍🏫 Ustoz kerak")],
    [KeyboardButton("🎓 Shogirt kerak")]
], resize_keyboard=True, row_width=1)

skip = ReplyKeyboardMarkup([[KeyboardButton("➡️ Tashlab ketish")]], resize_keyboard=True)

phone = ReplyKeyboardMarkup([[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]], resize_keyboard=True)

freelance = ReplyKeyboardMarkup([[KeyboardButton("🧑‍💻 Buyurtma berish")], [KeyboardButton("🚪 Bosh menu")]],
                                resize_keyboard=True, row_width=1)
