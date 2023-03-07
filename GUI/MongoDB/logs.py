from GUI.models.log import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Log
Документ: logs
"""


# получение записей о всех логах
def get_logs() -> MongoDBResult:
    res = db.logs.find()
    if res:
        logs = []
        for i in list(res):
            logs.append(Log(i))
        return MongoDBResult(True, logs)
    else:
        return MongoDBResult(False, [])


# получение записей о всех логах по статусу
def get_logs_by_status(status: LogStatus) -> MongoDBResult:
    res = db.logs.find({'status': status.value})
    if res:
        logs = []
        for i in list(res):
            logs.append(Log(i))
        return MongoDBResult(True, logs)
    else:
        return MongoDBResult(False, [])


# получение записей о всех логах по сервису
def get_logs_by_service(service: LogService) -> MongoDBResult:
    res = db.logs.find({'service': service.value})
    if res:
        logs = []
        for i in list(res):
            logs.append(Log(i))
        return MongoDBResult(True, logs)
    else:
        return MongoDBResult(False, [])


# добавление лога
def add_log(status, service, content):
    db.logs.insert_one({
        "date": datetime.now(),
        "status": status.value,
        "service": service.value,
        "content": str(content)
    })


# добавление логов
def add_logs(logs):
    db.logs.insert_many(logs)


# удаление лога по ID
def delete_log(id):
    db.logs.delete_one({
        '_id': ObjectId(id)
    })


# очистка Документа
def truncate():
    db.logs.drop()
