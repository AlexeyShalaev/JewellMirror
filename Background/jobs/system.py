import os

from Background.MongoDB.logs import add_log
from Background.models.log import LogService, LogStatus

gui_service = 'mirror_gui.service'
camera_service = 'mirror_camera.service'
services = [gui_service, camera_service]


def stop_system():
    for service in services:
        try:
            cmd = f'systemctl stop {service}'
            os.system(cmd)
        except Exception as ex:
            add_log(LogStatus.ERROR, LogService.BACKGROUND, ex)


def start_system():
    for service in services:
        try:
            cmd = f'systemctl start {service}'
            os.system(cmd)
        except Exception as ex:
            add_log(LogStatus.ERROR, LogService.BACKGROUND, ex)
