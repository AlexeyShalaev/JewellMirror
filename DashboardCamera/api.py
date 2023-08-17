import json
from datetime import datetime

import requests

from DashboardCamera.MongoDB.logs import add_log
from DashboardCamera.MongoDB.visits import add_unprocessed_visit
from DashboardCamera.config import load_config
from DashboardCamera.models.log import LogStatus, LogService

config = load_config()  # config
attendance_visit_url = f'{config.links.jewell}/api/attendance/visit'
qr_attendance_url = f'{config.links.jewell}/api/attendance/qrcode'
jewell_token = config.api.jewell


def send_attendance_visit(user_id, date):
    date = datetime.strftime(date, "%d.%m.%Y %H:%M:%S")
    return requests.post(attendance_visit_url,
                         json={"token": jewell_token,
                               'user_id': str(user_id),
                               'date': date})


def get_qr_visits_uri():
    r = requests.post(qr_attendance_url, json={"token": jewell_token})
    if r.ok:
        res = r.json()
        if res['success']:
            return config.links.jewell + res['uri']
    return None
