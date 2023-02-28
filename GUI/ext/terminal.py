import os

background_service = 'mirror_background.service'
camera_service = 'mirror_camera.service'


def get_background_status():
    return get_service_status(background_service)


def get_camera_status():
    return get_service_status(camera_service)


def get_service_status(service):
    cmd = f'systemctl status {service}'
    status = os.system(cmd)
    return status == 0
