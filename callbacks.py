from difflib import restore
from unittest import result
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile, InputFile

from responses import CONTACTS, FAQ
from aiogram.enums import ParseMode

from keyboards import get_back_menu, get_menu_buttons


async def get_prices(callback: CallbackQuery):
    file_path = "documents/services.pdf"
    await callback.message.answer("Цена на наши услуги: ")
    await callback.message.answer_document(
        FSInputFile(file_path), reply_markup=get_back_menu()
    )
    await callback.answer()


async def create_order(callback: CallbackQuery):
    await callback.message.answer("Вы нажали 'Помощь!'")
    await callback.answer()


async def get_contact(callback: CallbackQuery):
    result = "<b>Наши контакты:</b>\n\n"
    for key, value in CONTACTS.items():
        result += f"<b>{key}</b> : {value}\n\n"
    await callback.message.answer(
        text=result, parse_mode=ParseMode.HTML, reply_markup=get_back_menu()
    )
    await callback.answer()


async def get_faq(callback: CallbackQuery):
    result = "<b>Часто задаваемые вопросы:</b>\n\n"
    for val in FAQ:
        result += f"<b>Q: {val[0]}</b>\n A: {val[1]}\n\n"
    await callback.message.answer(
        text=result, parse_mode=ParseMode.HTML, reply_markup=get_back_menu()
    )
    await callback.answer()


async def menu_back(callback: CallbackQuery):
    photo = FSInputFile("img/logo.jpg")
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=get_menu_buttons(),
    )

    await callback.answer()
