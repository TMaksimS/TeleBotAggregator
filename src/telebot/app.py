import json
from datetime import datetime

import pydantic
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from settings import TOKEN_BOT
from src.telebot.schemas import MsRequest
from src.aggregator import Agreggator

BOT = Bot(token=TOKEN_BOT)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(text=f"Привет, {message.from_user.full_name}!")
    await message.answer(text="Я ожидаю от тебя данные в JSON формате\n"
                              "Вот пример:\n")
    await message.answer(text='`{"dt_from": "2022-10-01T00:00:00",'
                              ' "dt_upto": "2022-11-30T23:59:00",'
                              '   "group_type": "day"}`'
                         )

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
            await message.answer(text=str(res).replace("'", '"'))
        except ValueError:
            await message.answer(
                text="Даты указаны не в ISOformat "
                     "\nПринимаю дату типа %Y-%m-%dT%H:%M:%S"
                     "\nА group_type должен быть идентично одному из значений"
                     "\n(month, day, hour)"
            )
    except (json.JSONDecodeError, pydantic.ValidationError):
        await message.answer(text="Неккоректный запрос")
