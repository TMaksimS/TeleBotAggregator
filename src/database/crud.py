import bson

from src.database import mycoll

async def insert_data() -> None:
    """Метод вставляет в БД данные"""
    with open("src/database/sample_collection.bson", "rb") as f:
        data = bson.decode_all(f.read())
        mycoll.insert_many(data)
    return None


async def get_values(date_start, date_stop) -> int:
    """Метод возвращает сумму значений за выбранный период
    (изучить agreggator и $sum)"""
    query = {
        "dt": {
            "$gte": date_start,
            "$lt": date_stop
        }}
    res = [i["value"] for i in mycoll.find(query, {"_id": 0, "value": 1})]
    return sum(res)
