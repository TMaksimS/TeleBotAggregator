import asyncio

from src.database import mycoll
from src.database.crud import insert_data
from settings import LOGER


@LOGER.catch
async def check_data():
    """Проверяет наличие данных в датасете"""
    if mycoll.find_one() is None:
        await insert_data()
        LOGER.info("Данные были вставлены в БД")
    else:
        LOGER.info("Данные уже существую в БД")
        return None


if __name__ == "__main__":
    asyncio.run(check_data())
