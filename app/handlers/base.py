from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import FSInputFile

from app.keyboards.keyboards import get_main_menu, get_menu_buttons
from app.responses import HELP_INFO, WELCOME_INFO

router = Router()


@router.message(CommandStart())
async def send_welcome(message: Message) -> None:
    await message.answer(text=WELCOME_INFO, reply_markup=get_main_menu())


@router.message(Command("help"))
async def help_information(message: Message) -> None:
    await message.answer(text=HELP_INFO, parse_mode=ParseMode.HTML)


@router.message(Command("menu"))
async def menu_information(message: Message) -> None:
    photo = FSInputFile("img/logo.jpg")
    await message.answer_photo(
        photo=photo,
        reply_markup=get_menu_buttons(),
    )
