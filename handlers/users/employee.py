import re
from loader import dp, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.state import *
from keyboards.inline.main import confirm
from keyboards.default.main import main_markup, phone, skip


@dp.message_handler(state=EmployeeInfo.name)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"fullname": message.text})
    await message.answer(
        "Manzilingizni kiriting\nIltimos viloyat shahar nomlarini probel(\" \") bilan ajratib yozing huddi quyidagi "
        "misolda keltirilgandek\n\nMisol: <b>Xorazm Urganch</b>")
    await EmployeeInfo.next()


@dp.message_handler(state=EmployeeInfo.location)
async def freelance(message: types.Message, state: FSMContext):
    loc = message.text.split()
    if len(loc) >= 2:
        await state.update_data({"location": message.text})
        await message.answer(
            "Xodimni dasturlash tili yoki ishlatadigan dastur nomini kiritng\n\nMisol: "
            "<b>Python</b> yoki <b>3DMax</b>")
        await EmployeeInfo.next()
    else:
        await message.answer("Iltimos manzilingizni talab qilingan formatda yuboring\n\nMisol: <b>Xorazm Urganch</b>")


@dp.message_handler(state=EmployeeInfo.language)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"language": message.text})
    await message.answer(
        "Xodimning zarur mutaxassisligini yozing.\nMisol: <b>Android dasturlovchi</b> yoki <b>Video montajlovchi</b>")
    await EmployeeInfo.next()


@dp.message_handler(state=EmployeeInfo.speciality)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"special": message.text})
    await message.answer("Xodimni yosh chegarasini kiriting\n\nMisol: <b>20+</b> yoki <b>24-50</b>")
    await EmployeeInfo.next()


@dp.message_handler(state=EmployeeInfo.age_range)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    await message.answer("Siz (kompaniya, studia) bilan bog'lanish uchun raqam yuboring\n\nMisol: <b>+998991234567</b>")
    await EmployeeInfo.next()


@dp.message_handler(state=EmployeeInfo.phone)
async def freelance(message: types.Message, state: FSMContext):
    pattern = "^\+998([378]{2}|(9[013-57-9]))\d{7}$"
    string = message.text
    result = re.match(pattern, string)
    if result:
        await state.update_data({"phone": message.text})
        await message.answer(
            "Xodim qancha tajribaga ega bo'lishi kerakligini yozing son bilan\n\nMisol: <b>0</b> yoki <b>3+</b>")
        await EmployeeInfo.next()
    else:
        await message.answer("Iltimos telefon raqamini to'g'ri formatda kiritng\n\nMisol: <b>+998991234567</b>")


@dp.message_handler(state=EmployeeInfo.experience)
async def freelance(message: types.Message, state: FSMContext):
    pattern = "^[0-9.+-]{0,15}$"
    string = message.text
    result = re.match(pattern, string)
    if result:
        await state.update_data({"experience": message.text})
        await message.answer("Qo'shimcha ma'lumot bo'lsa yozing aks holda tashlab ketish tugmasini bosing",
                             reply_markup=skip)
        await EmployeeInfo.next()
    else:
        await message.answer("Iltimos tajribangizni to'g'ri formatda kiriting\n\nMisol: <b>1</b> yoki <b>0.5+</b>")


@dp.callback_query_handler(text="yes", state=EmployeeInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.send_copy(chat_id=ADMINS[0], reply_markup=confirm)
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()


@dp.callback_query_handler(text="no", state=EmployeeInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()


@dp.message_handler(state=EmployeeInfo.description)
async def freelance(message: types.Message, state: FSMContext):
    if message.text == "➡️ Tashlab ketish":
        data = await state.get_data()
        fin = f"Xodim kerak 👇\n\n" \
              f"Ish beruvchi: <b>{data.get('fullname')}</b>\n" \
              f"Yosh chegarasi: <b>{data.get('age')}</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Ish beruvchi manzili: <b>{data.get('location')}</b>\n" \
              f"Talab qilinadigan tajriba: <b>{data.get('experience')} yil</b>\n"
        await message.answer(fin, reply_markup=confirm)
        await state.finish()
    else:

        await state.update_data({"description": message.text})
        data = await state.get_data()
        fin = f"Xodim kerak 👇\n\n" \
              f"Ish beruvchi: <b>{data.get('fullname')}</b>\n" \
              f"Yosh chegarasi: <b>{data.get('age')}</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Ish beruvchi manzili: <b>{data.get('location')}</b>\n" \
              f"Talab qilinadigan tajriba: <b>{data.get('experience')} yil</b>\n" \
              f"Qo'shimcha ma'lumot: <i>{data.get('description')}</i>"
        await message.answer(fin, reply_markup=confirm)
    # await state.update_data({"user_id": message.from_user.id})
