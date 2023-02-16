from enum import Enum

import numpy as np
from bson import ObjectId


class Reward(Enum):
    TRIP = 'trip'  # поездка
    GRANT = 'grant'  # стипендия
    NULL = 'null'  # ничего


class Role(Enum):
    REGISTERED = 'registered'  # зарегистрированный пользователь, ждущий одобрения принятия
    STUDENT = 'student'  # студент
    TEACHER = 'teacher'  # учитель
    ADMIN = 'admin'  # админ
    NULL = 'null'  # ничего


class User:
    id: ObjectId
    telegram_id: int  # telegram chat id
    first_name: str  # alex
    role: Role  # student/teacher/admin
    reward: Reward  # trip/grant/none
    encodings: list

    def __init__(self, data):
        self.id = data['_id']
        self.telegram_id = data['telegram_id']
        self.first_name = data['first_name']
        self.role = Role(data['role'])
        self.reward = Reward(data['reward'])
        encodings = []
        for i in data['encodings']:
            encodings.append(np.fromstring(i, dtype=float, sep=","))
