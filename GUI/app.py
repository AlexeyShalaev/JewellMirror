import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from logging import getLogger

from flask import *
from flask_toastr import *

from ext.webui.api import api
from ext.webui.error import error
from ext.webui.view import view
from config import load_config

config = load_config()  # config
logger = getLogger(__name__)  # logging

# flask
app = Flask(config.flask.app_name)
app.register_blueprint(view)
app.register_blueprint(error)
app.register_blueprint(api)
app.config['SECRET_KEY'] = config.flask.secret_key

toastr = Toastr(app)


def main():
    logger.info("Starting app")
    app.run(debug=True, host='0.0.0.0')


if __name__ == "__main__":
    main()
