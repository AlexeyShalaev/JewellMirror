from GUI.models.visit import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Visit
Документ: visits
"""


# получение записей о всех посещаемостях
def get_visits() -> MongoDBResult:
    res = db.visits.find()
    if res:
        visits = []
        for i in list(res):
            visits.append(Visit(i))
        return MongoDBResult(True, visits)
    else:
        return MongoDBResult(False, [])


# получение посещаемости по ID
def get_visit_by_id(id) -> MongoDBResult:
    visit = db.visits.find_one({'_id': ObjectId(id)})
    if visit:
        return MongoDBResult(True, Visit(visit))
    else:
        return MongoDBResult(False, None)


# получение посещаемостей по User ID
def get_visits_by_user_id(user_id) -> MongoDBResult:
    res = db.visits.find({'user_id': ObjectId(user_id)})
    if res:
        visits = []
        for i in list(res):
            visits.append(Visit(i))
        return MongoDBResult(True, visits)
    else:
        return MongoDBResult(False, [])


# добавление посещаемости
def add_visit(user_id, date, visit_type, courses):
    db.visits.insert_one({
        "user_id": ObjectId(user_id),
        "date": date,
        "visit_type": visit_type.value,
        "courses": courses
    })


# добавление посещаемостей
def add_visits(visits):
    db.visits.insert_many(visits)


# удаление посещаемости по ID
def delete_visit(id):
    db.visits.delete_one({
        '_id': ObjectId(id)
    })


# очистка Документа
def visits_truncate():
    db.visits.drop()
