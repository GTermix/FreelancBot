from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import ADMINS
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from states.state import FreelanceInfo, MainState
from keyboards.default.main import freelance, skip, phone, main_markup, back
from keyboards.inline.main import confirm, salary, confirm_admin

summa = ""


@dp.message_handler(text="⚡️ Tezkor buyurtmalar (Freelance)", state=MainState.command)
async def freel(message: types.Message, state: FSMContext):
    await message.answer("Foydalanuvchi siz tezkor buyurtmalar bo'limidasiz. Bu bo'limda siz buyurtmalar berasiz."
                         "\nMisol: bot yasash, android dastur tuzish va hokozo. buyurtmalar uchun tugmalardan "
                         "foydalaning 👇", reply_markup=freelance)
    await FreelanceInfo.assign.set()


@dp.message_handler(state=FreelanceInfo.assign)
async def free(message: types.Message, state: FSMContext):
    if message.text == "🧑‍💻 Buyurtma berish":
        await message.answer("Loyiha (proyekt) nomini.\nMisollar: <b>Telegram kirdi chiqdi bot</b>, <b>Suhbat dasturi "
                             "(apk fayl)</b>, <b>Android uchun o'yin</b>, <b>Komyputer uchun dastur</b> va hokozo.",
                             reply_markup=back)
        await FreelanceInfo.name.set()


@dp.message_handler(state=FreelanceInfo.name)
async def free(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("Dastur yaratilishi kerak bo'lgan tilni kiriting.\nMisollar: Telegram bot -> PHP yoki Python, "
                         "Android dastur -> Java yoki Kotlin, Web-sayt -> Django yoki PHP, Android (Kompyuter) "
                         "o'yinlari -> C++ yoki o'yin yasash dasturlar(Unreal Engine, Buildbox, Unity3d vahokozo)")
    await FreelanceInfo.next()


@dp.message_handler(state=FreelanceInfo.language)
async def free(message: types.Message, state: FSMContext):
    await state.update_data({"language": message.text})
    await message.answer("Siz bilan bog'lanish uchun tugma orqali telefon raqamingizni kiriting", reply_markup=phone)
    await FreelanceInfo.next()


@dp.message_handler(content_types=['contact'], state=FreelanceInfo.phone)
async def freelance_df(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer("Raqam saqlandi", reply_markup=ReplyKeyboardRemove())
    await message.answer("Ish uchun ish haqqini kiriting. Summa dollar(USD, $ )da hisoblanadi.\nMisol 200 -> 200 $",
                         reply_markup=salary)
    await FreelanceInfo.next()


@dp.callback_query_handler(text="done", state=FreelanceInfo.work_price)
async def callme(call: types.CallbackQuery, state: FSMContext):
    global summa
    for i in range(len(summa)):
        if summa.startswith("0") or summa.startswith(" "):
            summa = summa[1:]
    if summa == "":
        summa = "tekin"
    await state.update_data({"salary": summa})
    await call.message.edit_text(f"Bajarildi!\nSumma saqlandi\nSumma {summa} $", reply_markup=None)
    await call.message.answer("Ish uchun ajratilgan vaqtni kiriting misol uchun 7 kun")
    summa = ""
    await FreelanceInfo.next()


@dp.callback_query_handler(text="clear", state=FreelanceInfo.work_price)
async def callme(call: types.CallbackQuery):
    global summa
    summa = "0"
    await call.message.edit_text(f"Joriy kiritmoqchi bo'lgan summangiz: <b>{summa} $</b>", reply_markup=salary)
    summa = ""


@dp.callback_query_handler(text="yes", state=FreelanceInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.send_copy(chat_id=ADMINS[0], reply_markup=confirm_admin(call.from_user.id))
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.callback_query_handler(text="no", state=FreelanceInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.callback_query_handler(state=FreelanceInfo.work_price)
async def callme(call: types.CallbackQuery):
    global summa
    summa += call.data
    await call.message.edit_text(f"Joriy kiritmoqchi bo'lgan summangiz: <b>{summa} $</b>", reply_markup=salary)


@dp.message_handler(lambda message: message.text.isdigit(), state=FreelanceInfo.time_limit)
async def work_tm(message: types.Message, state: FSMContext):
    await state.update_data({"time_limit": message.text})
    await message.answer(
        "Ish haqida ma'lumot kiriting misol uchun qandaydir dastur qandaydir kutubxonalardan foydalanilishi yoki f"
        "reelancer sheriklikada ishlashi kerakligi va hokozo")
    await FreelanceInfo.next()


@dp.message_handler(state=FreelanceInfo.work_information)
async def work_tm(message: types.Message, state: FSMContext):
    await state.update_data({"work_info": message.text})
    await message.answer("Ish uchun qat'iy qonunlar bo'lsa yozing aks holda tashlab ketish tugmasini bosing",
                         reply_markup=skip)
    await FreelanceInfo.next()


@dp.message_handler(state=FreelanceInfo.conditions)
async def work_tm(message: types.Message, state: FSMContext):
    await state.update_data({"condition": message.text})
    data = await state.get_data()
    if message.text != "➡️ Tashlab ketish":
        fin = f"⭕️ Tezkor buyurtma ⭕️\n\n" \
              f"Ish nomi: <b>{data.get('name')}</b>\n" \
              f"Dasturlash tili yoki dastur(ishni bajarish uchun majburiyat): <b>{data.get('language')}</b>\n" \
              f"Bog'lanish uchun raqam: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Belgilangan ish haqqi: <b>{data.get('salary')}</b>\n" \
              f"Buyurtma bajarilishi kerak bo'lgan vaqt: <b>{data.get('time_limit')}</b>\n" \
              f"Ish haqida ma'lumot: <b>{data.get('work_info')}</b>\n" \
              f"Shartlari: <b>{data.get('condition')}</b>"
    else:
        fin = f"⭕️ Tezkor buyurtma ⭕️\n\n" \
              f"Ish nomi: <b>{data.get('name')}</b>\n" \
              f"Dasturlash tili yoki dastur(ishni bajarish uchun majburiyat): <b>{data.get('language')}</b>\n" \
              f"Bog'lanish uchun raqam: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Belgilangan ish haqqi: <b>{data.get('salary')}</b>\n" \
              f"Buyurtma bajarilishi kerak bo'lgan vaqt: <b>{data.get('time_limit')}</b>\n" \
              f"Ish haqida ma'lumot: <b>{data.get('work_info')}</b>\n"
    await message.answer(fin, reply_markup=confirm)
    await FreelanceInfo.next()
