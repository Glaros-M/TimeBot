import datetime
from typing import NamedTuple, Optional
import database
from sqlalchemy.orm import Session


class ActionCreate(NamedTuple):
    name: str
    create_date: datetime.date
    create_datetime: datetime.datetime
    create_time: datetime.time

    @property
    def dict(self):
        """При использовании pydantic функция __dict__ для обьектов класса - доступна, а тут нет. Хз"""
        dict = {}
        dict.update({"name": self.name})
        dict.update({"create_date": self.create_date})
        dict.update({"create_datetime": self.create_datetime})
        dict.update({"create_time": self.create_time})

        return dict


class Action(ActionCreate):
    id: int


    def str(self):
        return f"{self.id=}{self.name=}{self.create_date=}{self.create_datetime=}{self.create_time=}"


def add_action(message: str) -> ActionCreate:
    name = message
    create_datetime = datetime.datetime.now()
    create_date = create_datetime.date()
    create_time = create_datetime.time()
    action = ActionCreate(name, create_date, create_datetime, create_time)
    return action


def get_all_actions(db: Session):
    actions_from_db: list[database.ActionsDB] = database.get_all_actions(db)
    ans = []
    for action_from_db in actions_from_db:
        ans.append(Action(id=action_from_db.id,
                          name=action_from_db.name,
                          create_date=action_from_db.create_date,
                          create_datetime=action_from_db.create_datetime,
                          create_time=action_from_db.create_time))
    return ans

def get_last_action():
    pass



if __name__ == "__main__":
    #a = Action(1, "123", datetime.date.today(), datetime.datetime.now(), datetime.datetime.now().time())
    b = Action(name="123", create_date=datetime.date.today(), create_datetime=datetime.datetime.now(), create_time=datetime.datetime.now().time())

    print()

