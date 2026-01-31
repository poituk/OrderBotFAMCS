import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import callbacks
from responses import HELP_INFO, WELCOME_INFO
from aiogram.types import FSInputFile
from aiogram import F


from keyboards import get_menu_buttons, get_main_menu
from callbacks import *

from config import API_TOKEN


bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.callback_query.register(callbacks.get_prices, F.data == "prices")
dp.callback_query.register(callbacks.create_order, F.data == "order")
dp.callback_query.register(callbacks.get_contact, F.data == "contact")
dp.callback_query.register(callbacks.get_faq, F.data == "faq")
dp.callback_query.register(callbacks.menu_back, F.data == "menu")


@dp.message(CommandStart())
async def send_welcome(message: Message) -> None:
    await message.answer(text=WELCOME_INFO, reply_markup=get_main_menu())


@dp.message(Command("help"))
async def help_information(message: Message) -> None:
    await message.answer(text=HELP_INFO, parse_mode=ParseMode.HTML)


@dp.message(Command("menu"))
async def menu_information(message: Message) -> None:
    photo = FSInputFile("img/logo.jpg")
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        reply_markup=get_menu_buttons(),
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
