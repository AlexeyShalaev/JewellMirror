import os
import threading
import time
from logging import getLogger

import requests
from flask import *

from MusicPlayer.MongoDB.songs import get_song_by_id, get_songs_json
from MusicPlayer.misc.music_player import MusicPlayer

logger = getLogger(__name__)  # logging
music = Blueprint('music', __name__, url_prefix='/music', template_folder='../templates', static_folder='../assets')

music_player = MusicPlayer()


# Установка события для окончания трека

def looped_music():
    time.sleep(5)
    while True:
        requests.get('http://127.0.0.1:5050/music/update_state')
        time.sleep(1)  # Задержка на 1 секунду


playing_thread = threading.Thread(target=looped_music, daemon=True)
playing_thread.start()


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@music.route('/', methods=["GET", "POST"])
def music_home():
    if request.method == "POST":
        try:
            r = get_song_by_id(request.form['btn_music_player'])
            if r.success:
                music_player.add_song(r.data)
                if music_player.current_song is None:
                    music_player.play_next_track()
        except Exception as ex:
            pass

    return render_template("music/player.html", songs=get_songs_json())


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@music.route('/songs/images/<song_id>', methods=["GET"])
def music_song_image(song_id):
    filename = 'default.png'
    directory = os.path.join(music_player.music_folder, 'images')
    try:
        files = os.listdir(directory)
        for file in files:
            if song_id == file.split('.')[0]:
                filename = file
                break
    except Exception as ex:
        pass

    return send_file(os.path.join(directory, filename))


@music.route('/player/json', methods=["GET"])
def music_player_json():
    return json.dumps(music_player.to_json()), 200, {'ContentType': 'application/json'}


@music.route('/player/change/mode', methods=["GET"])
def music_player_change_mode():
    if music_player.current_song is not None:
        if music_player.is_paused:
            music_player.resume()
        else:
            music_player.pause()
    else:
        music_player.play_next_track()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@music.route('/player/change/mute', methods=["GET"])
def music_player_change_mute():
    if music_player.is_muted:
        music_player.unmute()
    else:
        music_player.mute()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@music.route('/player/change/volume', methods=["POST"])
def music_player_change_volume():
    volume = int(request.form['volume']) / 100
    music_player.change_volume(volume)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@music.route('/player/skip', methods=["GET"])
def music_player_skip_song():
    music_player.skip_song()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@music.route('/update_state', methods=["GET"])
def music_update_state():
    music_player.play_loop()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
