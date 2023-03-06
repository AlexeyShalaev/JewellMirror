from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Timetable
Документ: timetables
"""


# проверка расписания по имени
def check_timetable_by_name(name: str) -> bool:
    res = db.timetables.find_one({'name': name})
    if res:
        return True
    return False


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
def timetables_truncate():
    db.timetables.drop()
