import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from logging import getLogger

from flask import *

from webui.routes.music import music as music_route
from webui.routes.api import api as api_route
from config import load_config

config = load_config()  # config
logger = getLogger(__name__)  # logging

# flask
app = Flask(config.flask.app_name)
app.register_blueprint(music_route)
app.register_blueprint(api_route)
app.config['SECRET_KEY'] = config.flask.secret_key


def main():
    logger.info("Starting app")
    app.run(host='0.0.0.0', port=5050)


if __name__ == "__main__":
    main()
