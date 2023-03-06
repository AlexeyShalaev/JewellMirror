from DashboardCamera.models.timetable import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Timetable
Документ: timetables
"""


def get_timetables() -> MongoDBResult:
    res = db.timetables.find()
    if res:
        timetables = []
        for i in list(res):
            timetables.append(Timetable(i))
        return MongoDBResult(True, timetables)
    else:
        return MongoDBResult(False, [])


def get_timetable_by_name(name: str) -> MongoDBResult:
    timetable = db.timetables.find_one({'name': name})
    if timetable:
        return MongoDBResult(True, Timetable(timetable))
    else:
        return MongoDBResult(False, None)


def add_timetable(name, days):
    db.timetables.insert_one({
        "name": name,
        "days": days
    })


def add_timetables(timetables):
    db.timetables.insert_many(timetables)


def update_timetable(name, days):
    db.timetables.update_one({'name': name}, {"$set": {'days': days}})


# очистка Документа
def truncate():
    db.timetables.drop()
