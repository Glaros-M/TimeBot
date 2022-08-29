import datetime
from typing import NamedTuple, Optional


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


if __name__ == "__main__":
    #a = Action(1, "123", datetime.date.today(), datetime.datetime.now(), datetime.datetime.now().time())
    b = Action(name="123", create_date=datetime.date.today(), create_datetime=datetime.datetime.now(), create_time=datetime.datetime.now().time())

    print()

