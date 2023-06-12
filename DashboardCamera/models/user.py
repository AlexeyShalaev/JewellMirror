from dataclasses import dataclass
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


class Sex(Enum):
    MALE = 'male'  # М
    FEMALE = 'female'  # Ж
    NULL = 'null'  # ничего


@dataclass
class FaceID:
    encodings: list  # face encodings
    greeting: str  # приветствие

    def __init__(self, data):
        self.encodings = [np.array(i) for i in data.get('encodings', [])]
        self.greeting = data.get('greeting', None)


class User:
    id: ObjectId
    telegram_id: int  # telegram chat id
    first_name: str  # alex
    last_name: str  # shalaev
    role: Role  # student/teacher/admin
    reward: Reward  # trip/grant/none
    face_id: FaceID

    def __init__(self, data):
        try:
            self.id = data['_id']
            self.telegram_id = data['telegram_id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.role = Role(data['role'])
            self.reward = Reward(data['reward'])
            self.face_id = FaceID(data.get('face_id', {}))
        except Exception as ex:
            print(ex)
