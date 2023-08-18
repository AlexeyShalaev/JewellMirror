import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from logging import getLogger

from flask import *
from flask_login import *

from ext.user_login import UserLogin
from ext.webui.api import api
from ext.webui.mirror import mirror as mirror_route
from ext.webui.music import music as music_route
from config import load_config

config = load_config()  # config
logger = getLogger(__name__)  # logging

# flask
app = Flask(config.flask.app_name)
app.register_blueprint(mirror_route)
app.register_blueprint(music_route)
app.register_blueprint(api)
app.config['SECRET_KEY'] = config.flask.secret_key

login_manager = LoginManager(app)
login_manager.login_view = 'mirror.login'
login_manager.login_message = "Авторизуйтесь для доступа к этой странице"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(id):
    return UserLogin(id, config.auth.login)


def main():
    logger.info("Starting app")
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
