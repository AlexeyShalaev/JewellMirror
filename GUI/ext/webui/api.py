from logging import getLogger

import requests
from bs4 import BeautifulSoup
from flask import *

from GUI.ext.tools import shabbat

logger = getLogger(__name__)  # logging
api = Blueprint('api', __name__, url_prefix='/api', template_folder='templates', static_folder='assets')


@api.route('/shabbat/kabbalat', methods=['POST'])
def shabbat_kabbalat():
    try:
        url = 'https://jewellclub.ru/shabbat/kabbalat-shabbat/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quote = soup.find('div', class_='one-activity__date-counter')
        remaining_seats = quote.find('b').text
        if int(remaining_seats) >= 0:
            return json.dumps({'success': True, 'seats': remaining_seats}), 200, {'ContentType': 'application/json'}
    except Exception as ex:
        logger.error(ex)
    return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


@api.route('/shabbat', methods=['POST'])
def shabbat_api():
    try:
        return json.dumps({'success': True, 'shabbat': shabbat()}), 200, {'ContentType': 'application/json'}
    except Exception as ex:
        logger.error(ex)
    return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
