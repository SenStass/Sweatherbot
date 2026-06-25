import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import menu, weather

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(weather.router)
    dp.include_router(menu.router)

    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
