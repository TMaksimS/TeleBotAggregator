import datetime

from typing import Any

from src.database.crud import get_values

b = {
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month"
}


class Agreggator:
    """Обьект агрегатора"""

    def __init__(self, query: dict):
        self.date_start = datetime.datetime.strptime(
            query["dt_from"],
            "%Y-%m-%dT%H:%M:%S"
        )
        self.date_stop = datetime.datetime.strptime(
            query["dt_upto"],
            "%Y-%m-%dT%H:%M:%S"
        )
        self.group_by = query["group_type"]
        self.params = query
        self.res = {
            "dataset": [],
            "label": []
        }

    @staticmethod
    async def counter_by_date(dt_start, dt_stop) -> tuple[int, Any]:
        """Метод для получение данных из БД"""
        value, date = await get_values(dt_start, dt_stop), dt_start
        return value, date.isoformat()

    async def _l_group_hour(self) -> dict:
        """Метод группировки по часам"""
        result = self.res
        delta = int(
            (self.date_stop - self.date_start).total_seconds()
            / 60
            / 60
        )
        for i in range(1, delta + 2):
            if delta <= 0:
                data = await self.counter_by_date(
                    self.date_start + datetime.timedelta(hours=-1 + i),
                    self.date_stop
                )
                result["dataset"].append(data[0])
                result["label"].append(datetime.datetime.strptime(
                    data[1],
                    "%Y-%m-%dT%H:%M:%S"
                ).isoformat())
                break
            data = await self.counter_by_date(
                self.date_start + datetime.timedelta(hours=-1 + i),
                self.date_start + datetime.timedelta(hours=0 + i)
            )
            result["dataset"].append(data[0])
            result["label"].append(datetime.datetime.strptime(
                data[1],
                "%Y-%m-%dT%H:%M:%S"
            ).isoformat())
            delta -= 1
        return result

    async def _l_group_day(self) -> dict:
        """Метод группировки по дням"""
        result = self.res
        delta = int(
            (self.date_stop - self.date_start).total_seconds()
            / 60
            / 60
            / 24
        )
        for i in range(1, delta + 2):
            if delta <= 0:
                data = await self.counter_by_date(
                    self.date_start + datetime.timedelta(days=-1 + i),
                    self.date_stop
                )
                result["dataset"].append(data[0])
                result["label"].append(datetime.datetime.strptime(
                    data[1],
                    "%Y-%m-%dT%H:%M:%S"
                ).isoformat())
                break
            data = await self.counter_by_date(
                self.date_start + datetime.timedelta(days=-1 + i),
                self.date_start + datetime.timedelta(days=0 + i)
            )
            result["dataset"].append(data[0])
            result["label"].append(datetime.datetime.strptime(
                data[1],
                "%Y-%m-%dT%H:%M:%S"
            ).isoformat())
            delta -= 1
        return result

    async def _pool_dates(self):
        """Метод создает диапозоны дат для группировки по месяцам"""
        dates = []
        dt_start, dt_stop = self.date_start, self.date_stop
        interval_date = self.date_start
        delta = (dt_stop - dt_start).days
        for i in range(1, delta + 1):
            interval_date += datetime.timedelta(days=1)
            if str(interval_date.date()).split("-")[1] > str(dt_start.date()).split("-")[1]:
                dates.append([dt_start, interval_date])
                dt_start = interval_date
            if i >= delta:
                dates.append([dt_start, dt_stop + datetime.timedelta(seconds=1)])
        return dates

    async def _l_group_month(self):
        """Метод группировки по месяцам"""
        result = self.res
        pool_dates = await self._pool_dates()
        for date in pool_dates:
            values = await self.counter_by_date(date[0], date[1])
            result["dataset"].append(values[0])
            result["label"].append(values[1])
        return result

    async def main(self):
        """Главная функция, которая отслеживает тип агреггации
         и назначет нужный алгоритм"""
        if self.group_by == "day":
            return await self._l_group_day()
        if self.group_by == "hour":
            return await self._l_group_hour()
        if self.group_by == "month":
            return await self._l_group_month()
