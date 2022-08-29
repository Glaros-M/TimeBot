import datetime

import database
from db import engine, SessionLocal
from sqlalchemy.orm import Session
import database
import Actions


database.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    db = SessionLocal()
    a = database.get_all_actions(db)
    for i in a:
        print(i.__dict__)

    database.delete_action(db, 1)

    a = database.get_all_actions(db)
    for i in a:
        print(i.__dict__)

