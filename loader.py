import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from db.connect import startup_table
from handlers.first_commands import mainrouter
from data.config import TOKEN


dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    dp.startup.register(startup_table)
    dp.include_routers(
        mainrouter
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
