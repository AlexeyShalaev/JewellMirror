from bson.json_util import dumps

from GUI.models.song import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Song
Документ: songs
"""


# получение записей о всех песнях
def get_songs() -> MongoDBResult:
    res = db.songs.find()
    if res:
        songs = []
        for i in list(res):
            songs.append(Song(i))
        return MongoDBResult(True, songs)
    else:
        return MongoDBResult(False, [])


def get_songs_json():
    return dumps(list(db.songs.find()))


# получение записей о всех песнях по статусу
def get_songs_by_author(author: str) -> MongoDBResult:
    res = db.songs.find({'author': author})
    if res:
        songs = []
        for i in list(res):
            songs.append(Song(i))
        return MongoDBResult(True, songs)
    else:
        return MongoDBResult(False, [])


# получение по ID
def get_song_by_id(id) -> MongoDBResult:
    song = db.songs.find_one({'_id': ObjectId(id)})
    if song:
        return MongoDBResult(True, Song(song))
    else:
        return MongoDBResult(False, None)


# получение по названию
def get_song_by_name(name) -> MongoDBResult:
    song = db.songs.find_one({'name': name})
    if song:
        return MongoDBResult(True, Song(song))
    else:
        return MongoDBResult(False, None)


# добавление песни
def add_song(name, author, duration):
    db.songs.insert_one({
        "name": name,
        "author": author,
        "duration": duration
    })


# добавление песен
def add_songs(songs):
    db.songs.insert_many(songs)


# удаление песни по ID
def delete_song(id):
    db.songs.delete_one({
        '_id': ObjectId(id)
    })


# очистка Документа
def truncate():
    db.songs.drop()
