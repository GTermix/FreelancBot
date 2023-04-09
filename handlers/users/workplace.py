import re
from loader import dp, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.state import *
from keyboards.inline.main import confirm
from keyboards.default.main import main_markup, phone, skip


@dp.message_handler(state=WorkplaceInfo.name)
async def freelance(message: types.Message, state: FSMContext):
    fullname = message.text
    fn = ""
    for m in fullname:
        if m != " ":
            fn += m
    if fn.isalpha():
        if len(fullname.split()) >= 2:
            await state.update_data({"fullname": message.text})
            await message.answer("Yoshingizni son bilan kiriting\nMaksimum yosh chegarasi 45 yosh\n\nMisol: <b>18</b>")
            await WorkplaceInfo.next()
        else:
            await message.answer("Ismingiz va familyangizni kiriting !")
    else:
        await message.answer("Ismlarda faqat harflar bo'lishi kerak, ismingizni to'g'ri yozing !")


@dp.message_handler(state=WorkplaceInfo.age)
async def freelance(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 10 < int(message.text) < 50:
            age = message.text
            await state.update_data({"age": age})
            await message.answer(
                "Dasturlashda ishlatiladigan tilingizni kiriting\nDizayner yoki shunga o'xshash bo'lsangiz "
                "siz ishlaydigan dastur nomini\n\nMisol: <b>Python</b> yoki <b>3dMax</b>")
            await WorkplaceInfo.next()
        else:
            await message.answer("Yosh 10-50 oralig'ida bo'lishi kerak")
    else:
        await message.answer("Yoshingizni sonlarda kiriting")


@dp.message_handler(state=WorkplaceInfo.language)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"language": message.text})
    await message.answer("Mutaxassisligingizni yozing.\nMisol: <b>Android dasturchi</b> yoki <b>Web dasturchi</b>")
    await WorkplaceInfo.next()


@dp.message_handler(state=WorkplaceInfo.speciality)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"special": message.text})
    await message.answer("Pastdagi tugma orqali raqamingizni yuboring 👇", reply_markup=phone)
    await WorkplaceInfo.next()


@dp.message_handler(content_types=['contact'], state=WorkplaceInfo.phone)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer(
        "Manzilingizni kiriting\nIltimos viloyat shahar nomlarini probel(\" \") bilan ajratib yozing huddi quyidagi "
        "misolda keltirilgandek\n\nMisol: <b>Xorazm Urganch</b>",
        reply_markup=ReplyKeyboardRemove())
    await WorkplaceInfo.next()


@dp.message_handler(state=WorkplaceInfo.location)
async def freelance(message: types.Message, state: FSMContext):
    loc = message.text.split()
    if len(loc) >= 2:
        await state.update_data({"location": message.text})
        await message.answer(
            "Tajribangizni yilda kiriting\nDiqqat bu ma'lumot faqat yilda hisoblanadi\n\nMisol: "
            "<b>1</b> yoki <b>0.5+</b>")
        await WorkplaceInfo.next()
    else:
        await message.answer("Iltimos manzilingizni talab qilingan formatda yuboring\n\nMisol: <b>Xorazm Urganch</b>")


@dp.message_handler(state=WorkplaceInfo.experience)
async def freelance(message: types.Message, state: FSMContext):
    pattern = "^[0-9.+-]{0,15}$"
    string = message.text
    result = re.match(pattern, string)
    if result:
        await state.update_data({"experience": message.text})
        await message.answer("Qo'shimcha ma'lumot bo'lsa yozing aks holda tashlab ketish tugmasini bosing",
                             reply_markup=skip)
        await WorkplaceInfo.next()
    else:
        await message.answer("Iltimos tajribangizni to'g'ri formatda kiriting\n\nMisol: <b>1</b> yoki <b>0.5+</b>")


@dp.callback_query_handler(text="yes", state=WorkplaceInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.send_copy(chat_id=ADMINS[0], reply_markup=confirm)
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()


@dp.callback_query_handler(text="no", state=WorkplaceInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()


@dp.message_handler(state=WorkplaceInfo.description)
async def freelance(message: types.Message, state: FSMContext):
    if message.text == "➡️ Tashlab ketish":
        data = await state.get_data()
        fin = f"Ish joyi kerak ma'lumotlar 👇\n\n" \
              f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n"
        await message.answer(fin, reply_markup=confirm)
        await state.finish()
    else:
        await state.update_data({"description": message.text})
        data = await state.get_data()
        fin = f"Ish joyi kerak ma'lumotlar 👇\n\n" \
              f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n" \
              f"Qo'shimcha ma'lumot: <i>{data.get('description')}</i>"
        await message.answer(fin, reply_markup=confirm)
    await WorkplaceInfo.next()
    await state.update_data({"user_id": message.from_user.id})
