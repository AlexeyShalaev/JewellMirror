from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью User
Документ: users
"""


# добавление пользователей
def add_users(users):
    db.users.insert_many(users)


# очистка Документа
def users_truncate():
    db.users.drop()
