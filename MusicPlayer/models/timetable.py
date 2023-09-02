from dataclasses import dataclass

from bson import ObjectId


@dataclass
class Timetable:
    id: ObjectId  # ID расписания
    name: str  # название расписания
    days: list  # расписание по дням

    def __init__(self, data):
        self.id = data['_id']
        self.name = data['name']
        self.days = data['days']
