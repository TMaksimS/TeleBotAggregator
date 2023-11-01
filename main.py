import asyncio
import logging

from src.telebot.app import BOT, dp
from settings import LOGER


@LOGER.catch
async def main():
    """Корутина запуска бота"""
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
