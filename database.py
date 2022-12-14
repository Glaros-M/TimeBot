import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date, DateTime, Time
from db import Base, SessionLocal
#from actions import ActionCreate, Action
# CRUD выносят в отдельный файл для избежания циклического импорта


class ActionsDB(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    user_telegram_id = Column(String, index=True)
    name = Column(String, index=True)
    create_date = Column(Date, index=True)
    create_datetime = Column(DateTime, index=True)
    create_time = Column(Time, index=True)

    def __repr__(self):
        return f"{self.id}, {self.user_telegram_id}, {self.name}, {self.create_date}, {self.create_datetime}, {self.create_time}"

    def __str__(self):
        return self.__repr__()


def dump_db() -> str:
    data = get_all_actions()
    out = ""
    for line in data:
        out+= str(line) + "\n"
    return out


def dump_db_to_file(path: str) -> None:
    data = dump_db()
    f = open(path, "w", encoding="utf8")
    f.write(data)
    f.close()


def get_all_actions() -> list[ActionsDB]:
    db: Session = SessionLocal()
    a = db.query(ActionsDB).all()
    db.close()
    return a


def get_all_actions_by_day(date: datetime.date, user_id: int) -> list[ActionsDB]:
    db: Session = SessionLocal()
    ans = db.query(ActionsDB).filter_by(create_date=date, user_telegram_id=user_id).order_by("create_datetime").all()
    db.close()
    return ans


def create_action(action) -> ActionsDB:
    db: Session = SessionLocal()
    db_action = ActionsDB(**action.__dict__)
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    db.close()
    return db_action


def delete_action(id: int) -> None:
    db: Session = SessionLocal()
    db_action = db.get(ActionsDB, id)
    if db_action:
        db.delete(db_action)
        db.commit()
    else:
        db.close()
        raise Exception(f"Action {id=} not found!")
    db.close()


def get_last_action() -> ActionsDB:
    db: Session = SessionLocal()
    action = db.query(ActionsDB).order_by(ActionsDB.create_datetime.desc()).first()
    return action


if __name__ == "__main__":
    print(dump_db())