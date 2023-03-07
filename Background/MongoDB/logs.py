from Background.models.log import *

from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Log
Документ: logs
"""


# добавление лога
def add_log(status, service, content):
    db.logs.insert_one({
        "date": datetime.now(),
        "status": status.value,
        "service": service.value,
        "content": str(content)
    })


# очистка Документа
def logs_truncate():
    db.logs.drop()
