import os

gui_service = 'mirror_gui.service'
camera_service = 'mirror_camera.service'
services = [gui_service, camera_service]


def stop_system():
    for service in services:
        cmd = f'systemctl stop {service}'
        os.system(cmd)


def start_system():
    for service in services:
        cmd = f'systemctl start {service}'
        os.system(cmd)
