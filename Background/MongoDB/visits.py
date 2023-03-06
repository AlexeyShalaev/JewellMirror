from . import db, MongoDBResult

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
