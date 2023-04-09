from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import ADMINS
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from states.state import FreelanceInfo
from keyboards.default.main import freelance, skip, phone, main_markup
from keyboards.inline.main import confirm, salary

summa = ""


@dp.message_handler(text="⚡️ Tezkor buyurtmalar (Freelance)", state="*")
async def freel(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    await message.answer("Foydalanuvchi siz tezkor buyurtmalar bo'limidasiz. Bu bo'limda siz buyurtmalar berasiz."
                         "\nMisol: bot yasash, android dastur tuzish va hokozo. buyurtmalar uchun tugmalardan "
                         "foydalaning 👇", reply_markup=freelance)


@dp.message_handler(text="🧑‍💻 Buyurtma berish")
async def free(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    await message.answer("Loyiha (proyekt) nomini.\nMisollar: <b>Telegram kirdi chiqdi bot</b>, <b>Suhbat dasturi "
                         "(apk fayl)</b>, <b>Android uchun o'yin</b>, <b>Komyputer uchun dastur</b> va hokozo.",
                         reply_markup=ReplyKeyboardRemove())
    await FreelanceInfo.name.set()


@dp.message_handler(text="🚪 Bosh menu", state=FreelanceInfo.name)
async def free(message: types.Message, state: FSMContext):
    if await state.get_data():
        await state.finish()
    await message.answer("Bosh menyudasiz kerakli bo'limni tanlang 👇", reply_markup=ReplyKeyboardRemove())


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
    await message.answer("Ish uchun ish haqqini kiriting. Summa dollar(USD, $ )da hisoblanadi.\nMisol 200 -> 200 $",
                         reply_markup=salary)
    await FreelanceInfo.next()


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
    await call.message.answer("Ish uchun ajratilgan vaqtni kiriting misol uchun 7 kun")
    summa = ""
    await FreelanceInfo.next()


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
    await bot.send_message(chat_id=ADMINS[0],
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
    await call.message.send_copy(chat_id=ADMINS[0], reply_markup=confirm)
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
    fin = f"Ish nomi: {data.get('name')}\n\n" \
          f"Dasturlash tili yoki dastur(ishni bajarish uchun majburiyat): {data.get('language')}\n\n" \
          f"Bog'lanish uchun raqam: "