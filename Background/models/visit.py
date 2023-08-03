from datetime import datetime

from bson import ObjectId
from pytz import timezone

tz = timezone('Europe/Moscow')


class UnprocessedVisit:
    id: ObjectId  # ID курса
    user_id: ObjectId  # ID пользователя
    date: datetime  # дата

    def __init__(self, data):
        self.id = data['_id']
        self.user_id = data['user_id']
        self.date = tz.localize(data['date'])  # datetime.strptime(data['date'], "%d.%m.%Y %H:%M:%S")
