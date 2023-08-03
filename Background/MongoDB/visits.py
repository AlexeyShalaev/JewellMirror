from bson import ObjectId

from . import db, MongoDBResult
from ..models.visit import UnprocessedVisit

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Visit
Документ: visits
"""


# добавление посещаемостей
def add_visits(visits):
    db.visits.insert_many(visits)


# очистка Документа
def visits_truncate():
    db.visits.drop()


def get_unprocessed_visits() -> MongoDBResult:
    res = db.unprocessed_visits.find()
    if res:
        visits = []
        for i in list(res):
            visits.append(UnprocessedVisit(i))
        return MongoDBResult(True, visits)
    else:
        return MongoDBResult(False, [])


def delete_unprocessed_visit(id):
    db.unprocessed_visits.delete_one({
        '_id': ObjectId(id)
    })
