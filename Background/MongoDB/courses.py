from Background.models.course import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Course
Документ: courses
"""


# получение записей о всех курсах
def get_courses() -> MongoDBResult:
    res = db.courses.find()
    if res:
        courses = []
        for i in list(res):
            courses.append(Course(i))
        return MongoDBResult(True, courses)
    else:
        return MongoDBResult(False, [])


# добавление курсов
def add_courses(courses):
    db.courses.insert_many(courses)


# очистка Документа
def truncate():
    db.courses.drop()
