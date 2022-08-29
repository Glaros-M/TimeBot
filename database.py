import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date, DateTime, Time
from db import Base
from Actions import ActionCreate, Action


class ActionsDB(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    create_date = Column(Date, index=True)
    create_datetime = Column(DateTime, index=True)
    create_time = Column(Time, index=True)


def get_all_actions(db: Session) -> list[Action]:
    a = db.query(ActionsDB).all()
    return a


def get_all_actions_by_day(db: Session, date: datetime.date) -> list[Action]:
    ans = db.query(ActionsDB).filter_by(create_date=date).all()
    return ans


def create_action(db: Session, action: ActionCreate) -> ActionsDB:
    db_action = ActionsDB(**action.dict)
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


def delete_action(db: Session, id: int) -> None:
    db_action = db.get(ActionsDB, id)
    if db_action:
        db.delete(db_action)
        db.commit()
    else:
        raise Exception(f"Action {id=} not found!")

if __name__ == "__main__":
    pass