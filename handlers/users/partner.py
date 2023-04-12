import re
from loader import dp, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.state import *
from keyboards.inline.main import confirm, salary,confirm_admin
from keyboards.default.main import main_markup, work_keyboard, phone, skip,back


@dp.message_handler(state=PartnerInfo.name)
async def freelance(message: types.Message, state: FSMContext):
    fullname = message.text
    fn = ""
    for m in fullname:
        if m != " ":
            fn += m
    if fn.isalpha():
        if len(fullname.split()) >= 2:
            await state.update_data({"fullname": message.text})
            await message.answer("Yoshingizni son bilan kiriting\nMaksimum yosh chegarasi 45 yosh\n\nMisol: <b>18</b>",
                                 reply_markup=back)
            await PartnerInfo.next()
        else:
            await message.answer("Ismingiz va familyangizni kiriting !")
    else:
        await message.answer("Ismlarda faqat harflar bo'lishi kerak, ismingizni to'g'ri yozing !")


@dp.message_handler(lambda message: message.text.isdigit(), state=PartnerInfo.age)
async def freelance(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 10 < int(message.text) < 50:
            age = message.text
            await state.update_data({"age": age})
            await message.answer(
                "Dasturlashda ishlatiladigan tilingizni kiriting\nDizayner yoki shunga o'xshash bo'lsangiz "
                "siz ishlaydigan dastur nomini\n\nMisol: <b>Python</b> yoki <b>3dMax</b>")
            await PartnerInfo.next()
        else:
            await message.answer("Yosh 10-50 oralig'ida bo'lishi kerak")
    else:
        await message.answer("Yoshingizni sonlarda kiriting")


@dp.message_handler(state=PartnerInfo.language)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"language": message.text})
    await message.answer("Pastdagi tugma orqali raqamingizni yuboring 👇", reply_markup=phone)
    await PartnerInfo.next()


@dp.message_handler(content_types=['contact'], state=PartnerInfo.phone)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer("Manzilingizni to'liq kiriting\n\nMisol: <b>Xorazm Urganch</b>",
                         reply_markup=back)
    await PartnerInfo.next()


@dp.message_handler(state=PartnerInfo.location)
async def freelance(message: types.Message, state: FSMContext):
    loc = message.text.split()
    if len(loc) >= 2:
        await state.update_data({"location": message.text})
        await message.answer(
            "Hozirda qayerda ishlashingiz yoki o'qishingizni yozing\n\nMisol: <b>Figma</b> yoki <b>TATU</b>")
        await PartnerInfo.next()
    else:
        await message.answer("Iltimos manzilingizni talab qilingan formatda yuboring\n\nMisol: <b>Xorazm Urganch</b>")


@dp.message_handler(state=PartnerInfo.work_time)
async def freelance(message: types.Message, state: FSMContext):
    await state.update_data({"work_time": message.text})
    await message.answer(
        "Tajribangizni yilda kiriting\nDiqqat bu ma'lumot faqat yilda hisoblanadi\n\nMisol: <b>1</b> yoki <b>0.5+</b>")
    await PartnerInfo.next()


@dp.message_handler(state=PartnerInfo.experience)
async def freelance(message: types.Message, state: FSMContext):
    pattern = "^[0-9.+-]{0,15}$"
    string = message.text
    result = re.match(pattern, string)
    if result:
        await state.update_data({"experience": message.text})
        await message.answer("Qo'shimcha ma'lumot bo'lsa yozing aks holda tashlab ketish tugmasini bosing",
                             reply_markup=skip)
        await PartnerInfo.next()
    else:
        await message.answer("Iltimos tajribangizni to'g'ri formatda kiriting\n\nMisol: <b>1</b> yoki <b>0.5+</b>")


@dp.callback_query_handler(text="yes", state=PartnerInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.send_copy(chat_id=ADMINS[0], reply_markup=confirm_admin(call.from_user.id))
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.callback_query_handler(text="no", state=PartnerInfo.done)
async def callme(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Kerakli bo'limni tanlang 👇", reply_markup=main_markup)
    await state.finish()
    await MainState.command.set()


@dp.message_handler(state=PartnerInfo.description)
async def freelance(message: types.Message, state: FSMContext):
    if message.text == "➡️ Tashlab ketish":
        data = await state.get_data()
        fin = f"Sherik kerak, o'zim haqimda\n\n" \
              f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Ish vaqti: <b>{data.get('work_time')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n"
        await message.answer(fin, reply_markup=confirm)
        await state.finish()
    else:
        await state.update_data({"description": message.text})
        data = await state.get_data()
        fin = f"Sherik kerak, o'zim haqimda\n\n" \
              f"Ismi: <b>{data.get('fullname')}</b>\n" \
              f"Yoshi: <b>{data.get('age')} yosh</b>\n" \
              f"Dasturlash tili (ishlatadigan dasturi): <b>{data.get('language')}</b>\n" \
              f"Telefon raqami: <b><span class=\"tg-spoiler\">{data.get('phone')}</span></b>\n" \
              f"Hozirgi manzili: <b>{data.get('location')}</b>\n" \
              f"Ish vaqti: <b>{data.get('work_time')}</b>\n" \
              f"Tajribasi: <b>{data.get('experience')} yil</b>\n" \
              f"Qo'shimcha ma'lumot: <i>{data.get('description')}</i>"
        await message.answer(fin, reply_markup=confirm)