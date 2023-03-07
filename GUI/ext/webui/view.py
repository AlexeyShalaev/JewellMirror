from datetime import datetime
from logging import getLogger

from flask import *

from flask_login import login_user, login_required, current_user, logout_user

from GUI.MongoDB.logs import get_logs
from GUI.MongoDB.users import get_users_by_role
from GUI.MongoDB.visits import get_visits
from GUI.ext.user_login import UserLogin
from GUI.ext import config
from GUI.ext.terminal import get_camera_status, get_background_status, process_service
from GUI.ext.tools import shabbat
from GUI.models.user import Role

logger = getLogger(__name__)  # logging
view = Blueprint('view', __name__, template_folder='templates', static_folder='assets')


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@view.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        try:
            if request.form['btn_service'] == 'stop':
                process_service('stop', request.form['service'])
            elif request.form['btn_service'] == 'run':
                process_service('start', request.form['service'])
        except Exception as ex:
            logger.error(ex)
    visits = get_visits().data
    users = get_users_by_role(Role.STUDENT).data
    logs = get_logs().data
    visits.sort(key=lambda x: x.date, reverse=True)
    visits_json = []
    users_dict = dict()
    for user in users:
        users_dict[user.id] = {
            'name': f'{user.first_name} {user.last_name}',
            'visits': 0
        }
    for visit in visits:
        js = {
            'user_id': visit.user_id,
            'type': visit.visit_type.value,
            'date': datetime.strftime(visit.date, f'%d.%m.%Y %H:%M:%S'),
            'courses': '/'.join(visit.courses),
            'user': users_dict[visit.user_id]['name']
        }
        users_dict[visit.user_id]['visits'] += 1
        visits_json.append(js)
    return render_template("home.html",
                           camera=get_camera_status(), background=get_background_status(),
                           visits=visits_json, users=users_dict, logs=logs)


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
