import json

from bson import ObjectId


class Song:
    id: ObjectId
    name: str
    author: str
    duration: int  # seconds

    def __init__(self, data):
        self.id = data['_id']
        self.name = data['name']
        self.author = data['author']
        self.duration = data['duration']

    def to_json(self):
        data = {
            "id": str(self.id),
            "name": self.name,
            "author": self.author,
            "duration": self.duration
        }
        return data
