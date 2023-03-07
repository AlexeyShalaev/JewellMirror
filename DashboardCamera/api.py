import json
from datetime import datetime

import requests

from DashboardCamera.MongoDB.logs import add_log
from DashboardCamera.config import load_config
from DashboardCamera.models.log import LogStatus, LogService

config = load_config()  # config
attendance_url = f'{config.links.jewell}/api/attendance/update'
jewell_token = config.api.jewell


async def update_user_attendance(user_id, date, count):
    try:
        user_id = str(user_id)
        date = datetime.strftime(date, "%d.%m.%Y %H:%M:%S")
        r = requests.post(attendance_url,
                          json={"token": jewell_token,
                                'user_id': user_id,
                                'date': date,
                                'count': count})
        if r.ok:
            res = r.json()
            if res['success']:
                return
        add_log(LogStatus.WARNING, LogService.CAMERA, f"Couldn't update attendance for {user_id} {date} {count}")
    except Exception as ex:
        add_log(LogStatus.ERROR, LogService.CAMERA, ex)
