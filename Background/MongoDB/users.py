from Background.models.user import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью User
Документ: users
"""


# получение записей о всех пользователях
def get_users() -> MongoDBResult:
    res = db.users.find()
    if res:
        users = []
        for i in list(res):
            users.append(User(i))
        return MongoDBResult(True, users)
    else:
        return MongoDBResult(False, [])


# добавление пользователей
def add_users(users):
    db.users.insert_many(users)


# очистка Документа
def truncate():
    db.users.drop()
