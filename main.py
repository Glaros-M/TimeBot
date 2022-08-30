import datetime

from db import engine, SessionLocal
from sqlalchemy.orm import Session
import database
import actions


import aiohttp
from aiogram import Bot, Dispatcher, executor, types

database.Base.metadata.create_all(bind=engine)



API_TOKEN = "1171530088:AAEY9EXzFxBXZm4_Bymzm18hYpm8KZjnpx8"     # os.getenv("TELEGRAM_API_TOKEN")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Сегодняшние действия: /actions")


@dp.message_handler(commands=['actions'])
async def get_day_actions(message: types.Message):
    """"""
    db = SessionLocal()
    getted_actions = actions.get_all_actions(db)
    str = "1"
    for act in getted_actions:
        str += act.str()

    await message.answer(str
        )



@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавление нового действия"""
    action = actions.add_action(message.text)
    answer_message = (
        f"Начато действие {action.name} в {action.create_datetime}.\n\n"
        f"Предыдущее: {123}")
    await message.answer(answer_message)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)