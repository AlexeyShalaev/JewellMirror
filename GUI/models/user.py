from enum import Enum

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
    last_name: str  # shalaev
    role: Role  # student/teacher/admin
    reward: Reward  # trip/grant/none

    def __init__(self, data):
        self.id = data['_id']
        self.telegram_id = data['telegram_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.role = Role(data['role'])
        self.reward = Reward(data['reward'])
