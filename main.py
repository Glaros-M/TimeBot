import datetime
#from aiogram.types import BotCommand
from aiogram import types
from db import engine, SessionLocal
from sqlalchemy.orm import Session
import database
import actions
from middlewares import AccessMiddleware


import aiohttp
from aiogram import Bot, Dispatcher, executor, types

database.Base.metadata.create_all(bind=engine)



API_TOKEN = "1171530088:AAEY9EXzFxBXZm4_Bymzm18hYpm8KZjnpx8"     # os.getenv("TELEGRAM_API_TOKEN")
ACCESS_LIST = [
    1115933014,
    1179070234
]


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_LIST))

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начало"),
        types.BotCommand(command="/categories", description="Базовые категории"),
        #BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Сегодняшние действия: /actions"
        )
    print(f"{message.from_user.id=}, {message.from_user.username=}, {message.from_user.last_name=}, {message.from_user.first_name=}")
    await set_commands(bot)


@dp.message_handler(commands=['categories'])
async def get_base_categories(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["test"]
    keyboard.add(*buttons)
    await message.answer("Выберите категорию из представленных или напечатайте свою: ", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись по её идентификатору"""
    row_id = int(message.text[4:])
    try:
        database.delete_action(row_id)
        answer_message = "Удалил"
    except Exception as e:
        answer_message = e

    await message.answer(answer_message)

@dp.message_handler(commands=['actions'])
async def get_day_actions(message: types.Message):
    """"""
    getted_actions = actions.get_all_actions()
    str = actions.convert_action_list_to_str(getted_actions)

    await message.answer(str, parse_mode="markdown")




@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавление нового действия"""
    action = actions.add_action(message)
    last_actions = actions.get_actions_by_date(datetime.date.today())
    str = actions.convert_action_list_to_str(last_actions)
    answer_message = (
        f"Начато действие {action.name} в {action.create_datetime}.\n\n"
        f"Предыдущие сегодня:\n "
        f"{str}")
    await message.answer(answer_message, parse_mode="markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
