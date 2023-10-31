import bson

from src.database import mycoll


async def insert_data() -> None:
    """Метод вставляет в БД данные"""
    with open("src/database/sample_collection.bson", "rb") as f:
        data = bson.decode_all(f.read())
        mycoll.insert_many(data)
    return None
