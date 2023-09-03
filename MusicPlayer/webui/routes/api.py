import os
import threading
from logging import getLogger

import requests_html
from flask import *

from MusicPlayer import config
from MusicPlayer.MongoDB.songs import delete_song, add_song, update_song
from MusicPlayer.misc.music_player import MusicPlayer
from MusicPlayer.misc.speech import say

logger = getLogger(__name__)  # logging
api = Blueprint('api', __name__, url_prefix='/api')

api_token = config.api_key

mp = MusicPlayer()


@api.route('/player/admin_permission', methods=["POST"])
def api_change_admin_permission():
    token = request.json['token']
    if token == api_token:
        admin_permission = request.json['admin_permission']
        mp.admin_permission = admin_permission
        if admin_permission is False:
            mp.pause()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/player/admin_permission/get', methods=["GET"])
def api_get_admin_permission():
    return json.dumps({'data': mp.admin_permission}), 200, {'ContentType': 'application/json'}


@api.route('/player/reload', methods=["POST"])
def api_reload_player():
    if request.json['token'] == api_token:
        mp.reload()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/songs/delete', methods=["POST"])
def api_delete_song():
    if request.json['token'] == api_token:
        song_id = request.json['song_id']

        mp.reload()

        delete_song(song_id)

        # Удалить mp3 файл
        mp3_file_path = os.path.join(mp.music_folder, 'audios', f'{song_id}.mp3')
        if os.path.exists(mp3_file_path):
            os.remove(mp3_file_path)

        # Удалить изображение
        images_dir = os.path.join(mp.music_folder, 'images')
        for file in os.listdir(images_dir):
            if song_id == file.split('.')[0]:
                os.remove(os.path.join(images_dir, file))
                break

        mp.reload()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/songs/add', methods=["POST"])
def api_add_song():
    if request.form['token'] == api_token:
        # Получение данных из формы
        song_name = request.form['song_name']
        song_author = request.form['song_author']
        mp3_file = request.files['mp3_file']
        image_file = request.files.get('image_file', None)

        song_id = str(add_song(song_name, song_author, 1).inserted_id)

        # Сохранение файлов
        mp3_path = os.path.join(mp.music_folder, 'audios', f'{song_id}.mp3')
        mp3_file.save(mp3_path)
        duration = mp.get_song_duration(mp3_path)
        if duration <= 0:
            delete_song(song_id)
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
        else:
            update_song(song_id, 'duration', duration)

            if image_file and image_file.filename:
                file_extension = os.path.splitext(image_file.filename)[-1]
                image_path = os.path.join(mp.music_folder, 'images', f'{song_id}{file_extension}')
                image_file.save(image_path)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/speech/say', methods=["POST"])
async def api_speech_say():
    token = request.json['token']
    if token == api_token:
        await say(request.json['text'])
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
