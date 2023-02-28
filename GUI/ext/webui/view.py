from logging import getLogger

from flask import *

from flask_login import login_user, login_required, current_user, logout_user

from GUI.ext.user_login import UserLogin
from GUI.ext import config
from GUI.ext.terminal import get_camera_status, get_background_status
from GUI.ext.tools import shabbat

logger = getLogger(__name__)  # logging
view = Blueprint('view', __name__, template_folder='templates', static_folder='assets')


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@view.route('/')
@login_required
def home():
    # todo post: download xlsx
    # todo get attendance
    return render_template("home.html", camera=get_camera_status(), background=get_background_status())


# Уровень:              Авторизация
# База данных:          -
# HTML:                 login
@view.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if username == config.auth.login and password == config.auth.password:
                login_user(UserLogin(1, config.auth.login))
                return redirect(url_for('view.home'))
        except Exception as ex:
            logger.error(ex)
    return render_template("login.html")


# Уровень:              logout
# База данных:          -
# HTML:                 -
@view.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("view.login"))


# Уровень:              Зеркало
# База данных:          -
# HTML:                 mirror
@view.route('/mirror')
@login_required
def mirror():
    return render_template("mirror.html", shabbat=shabbat())
