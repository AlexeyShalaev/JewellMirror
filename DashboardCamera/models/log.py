from datetime import datetime
from enum import Enum

from bson import ObjectId


class LogStatus(Enum):
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'


class LogService(Enum):
    BACKGROUND = 'background'
    CAMERA = 'camera'
    GUI = 'gui'


class Log:
    id: ObjectId
    date: datetime
    status: LogStatus
    service: LogService
    content: str

    def __init__(self, data):
        self.id = data['_id']
        self.date = data['date']
        self.content = data['content']
        self.service = LogService(data['service'])
        self.status = LogStatus(data['status'])
