from logging import getLogger

from flask import *

from GUI.ext.tools import shabbat

logger = getLogger(__name__)  # logging
view = Blueprint('view', __name__, template_folder='templates', static_folder='assets')


# Уровень:              Главная страница
# База данных:          -
# HTML:                 home
@view.route('/')
def home():
    return render_template("home.html", shabbat=shabbat())
