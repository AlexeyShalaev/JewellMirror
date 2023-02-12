from logging import getLogger

from flask import *

logger = getLogger(__name__)  # logging
error = Blueprint('error', __name__, template_folder='templates', static_folder='assets')
