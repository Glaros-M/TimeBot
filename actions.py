import datetime
from typing import NamedTuple, Optional
import database
from sqlalchemy.orm import Session
from aiogram import types


class ActionCreate():
    def __init__(self,
                 name: str,
                 user_telegram_id: str,
                 create_date: datetime.date,
                 create_datetime: datetime.datetime,
                 create_time: datetime.time):
        self.name = name
        self.user_telegram_id = user_telegram_id
        self.create_date = create_date
        self.create_datetime = create_datetime
        self.create_time = create_time


class Action(ActionCreate):

    def __init__(self,
                 id: int,
                 name: str,
                 user_telegram_id: str,
                 create_date: datetime.date,
                 create_datetime: datetime.datetime,
                 create_time: datetime.time):
        self.id = id
        super().__init__(name, user_telegram_id, create_date, create_datetime, create_time)

    def str(self):
        return f"*{self.name }* : _{self.create_date}_, {self.create_time}, /del{self.id}" #"{:<5}{:<20}{:<30}".format(self.id, self.name, str(self.create_datetime))


def convert_action_list_to_str(actions: list[Action]) -> str:
    str = ""
    for act in actions:
        str += act.str() + "\n"
    return str


def _get_clear_dict(obj: "database.ActionsDB"):
    """Не знаю как обойти лишний аргумент при распаковке словаря класса SQLAlchemy. Поэтому удаляю его"""
    dict1 = obj.__dict__
    del dict1["_sa_instance_state"]
    return obj.__dict__


def _parse_message_to_action(message: types.Message) -> ActionCreate:
    user_telegram_id = message.from_user.id
    name = message.text
    create_datetime = datetime.datetime.now()
    create_date = create_datetime.date()
    create_time = create_datetime.time()
    action = ActionCreate(name, user_telegram_id, create_date, create_datetime, create_time)
    return action


def add_action(message: types.Message) -> Action:
    action_for_db = _parse_message_to_action(message)
    action_from_db = database.create_action(action_for_db)
    # Не знаю как обойти лишний аргумент при распаковке словаря класса SQLAlchemy. Поэтому удаляю его
    #del action_from_db.__dict__["_sa_instance_state"]
    return Action(**_get_clear_dict(action_from_db))




def get_all_actions():
    actions_from_db: list[database.ActionsDB] = database.get_all_actions()
    ans = []
    for action_from_db in actions_from_db:
        ans.append(Action(id=action_from_db.id,
                          name=action_from_db.name,
                          create_date=action_from_db.create_date,
                          create_datetime=action_from_db.create_datetime,
                          create_time=action_from_db.create_time,
                          user_telegram_id=action_from_db.user_telegram_id))
    return ans


def get_actions_by_date(date: datetime.date):
    actionsDB = database.get_all_actions_by_day(date)
    actions: list[Action] = []
    for actiondb in actionsDB:
        actions.append(Action(**_get_clear_dict(actiondb)))
    return actions


def get_last_action():
    pass


if __name__ == "__main__":
    b = ActionCreate(name="123", create_date=datetime.date.today(), create_datetime=datetime.datetime.now(),
               create_time=datetime.datetime.now().time(), user_telegram_id="1")

    print(b.__dict__)
