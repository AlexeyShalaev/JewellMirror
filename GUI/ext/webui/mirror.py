import os
from logging import getLogger

from flask import *
from flask_login import login_user, login_required, current_user, logout_user

from GUI.MongoDB.logs import get_logs
from GUI.MongoDB.songs import get_songs, delete_song
from GUI.ext import config
from GUI.ext.data import manage_data
from GUI.ext.music_player import MusicPlayer
from GUI.ext.terminal import get_camera_status, get_background_status, process_service
from GUI.ext.tools import shabbat
from GUI.ext.user_login import UserLogin

logger = getLogger(__name__)  # logging
mirror = Blueprint('mirror', __name__, url_prefix='/mirror', template_folder='templates', static_folder='assets')


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@mirror.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        try:
            if request.form['btn_service'] == 'stop':
                process_service('stop', request.form['service'])
            elif request.form['btn_service'] == 'run':
                process_service('start', request.form['service'])
            elif request.form['btn_service'] == 'update':
                manage_data()
        except Exception as ex:
            logger.error(ex)

    logs = get_logs().data
    logs.sort(key=lambda x: x.date, reverse=True)

    return render_template("mirror/home.html",
                           camera=get_camera_status(), background=get_background_status(), logs=logs)


# Уровень:              Авторизация
# База данных:          -
# HTML:                 login
@mirror.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mirror.home'))
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if username == config.auth.login and password == config.auth.password:
                login_user(UserLogin(1, config.auth.login))
                return redirect(url_for('mirror.home'))
        except Exception as ex:
            logger.error(ex)
    return render_template("mirror/login.html")


# Уровень:              logout
# База данных:          -
# HTML:                 -
@mirror.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("mirror.login"))


# Уровень:              Зеркало
# База данных:          -
# HTML:                 interface
@mirror.route('/interface')
@login_required
def mirror_interface():
    return render_template("mirror/mirror.html", shabbat=shabbat())


# Уровень:              Музыка
# База данных:          -
# HTML:                 music
@mirror.route('/player', methods=["GET", "POST"])
@login_required
def mirror_admin_player():
    mp = MusicPlayer()

    if request.method == "POST":
        try:
            if request.form['btn_player'] == 'stop':
                mp.admin_permission = False
            elif request.form['btn_player'] == 'run':
                mp.admin_permission = True
            elif request.form['btn_player'] == 'reload':
                mp.reload()
            elif request.form['btn_player'] == 'delete_song':
                song_id = request.form['song_id']
                delete_song(song_id)

                # Удалить mp3 файл
                mp3_file_path = os.path.join(mp.music_folder, 'audios', f'{song_id}.mp3')
                if os.path.exists(mp3_file_path):
                    os.remove(mp3_file_path)

                # Удалить изображение
                images_dir = os.path.join(mp.music_folder, 'images')
                for file in os.listdir(images_dir):
                    if song_id == file.split('.')[0]:
                        os.remove(os.path.join(images_dir, song_id))
                        break

                mp.reload()

        except Exception as ex:
            logger.error(ex)

    return render_template("mirror/player.html", permission=mp.admin_permission, songs=get_songs().data)
