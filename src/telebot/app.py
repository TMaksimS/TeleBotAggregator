import json
from datetime import datetime

from aiogram import Bot, Dispatcher, types

from settings import TOKEN_BOT
from src.telebot.schemas import MsRequest
from src.aggregator import Agreggator

BOT = Bot(token=TOKEN_BOT)
dp = Dispatcher()


@dp.message()
async def msresponse(message: types.Message):
    """Обработчик сообщений"""
    try:
        ms_model = json.loads(message.text)
        a = MsRequest.model_validate(ms_model)
        try:
            datetime.strptime(a.dt_from, "%Y-%m-%dT%H:%M:%S")
            datetime.strptime(a.dt_upto, "%Y-%m-%dT%H:%M:%S")
            if str(a.group_type.lower()) not in ("month", "day", "hour"):
                raise ValueError
            ag = Agreggator(json.loads(message.text))
            res = await ag.main()
            await message.answer(text=str(res))
        except ValueError:
            await message.answer(
                text="Даты указаны не в ISOformat "
                     "\nПринимаю дату типа %Y-%m-%dT%H:%M:%S"
                     "\nА group_type должен быть идентично одному из значений"
                     "\n(month, day, hour)"
            )
    except Exception:  # json.JSONDecodeError, pydantic.ValidationError
        await message.answer(text="Неккоректный запрос")
