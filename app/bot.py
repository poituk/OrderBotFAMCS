import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher import router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.database import create_tables, recreate_tables


from app.handlers import router

from app.config import API_TOKEN

storage = MemoryStorage()
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

dp.include_router(router)


async def main() -> None:
    await create_tables()
    #await recreate_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
