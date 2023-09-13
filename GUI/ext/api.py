from datetime import datetime

import requests

from GUI.MongoDB.logs import add_log
from GUI.config import load_config
from GUI.models.log import LogStatus, LogService

config = load_config()  # config

users_url = f'{config.links.jewell}/api/users'
courses_url = f'{config.links.jewell}/api/courses'
attendance_url = f'{config.links.jewell}/api/attendance/update'

admin_permission_url = f'{config.links.music_player}/api/player/admin_permission'
mp_reload_url = f'{config.links.music_player}/api/player/reload'
delete_song_url = f'{config.links.music_player}/api/songs/delete'
add_song_url = f'{config.links.music_player}/api/songs/add'
get_admin_permission_url = f'{config.links.music_player}/api/player/admin_permission/get'

jewell_token = config.api.jewell
mp_token = config.api.music_player


def get_users_from_api() -> (bool, ...):
    return get_data_from_api(users_url)


def get_courses_from_api() -> (bool, ...):
    return get_data_from_api(courses_url)


def get_data_from_api(url: str) -> (bool, ...):
    try:
        r = requests.post(url, json={"token": jewell_token})
        if r.ok:
            res = r.json()
            if res['success']:
                return True, res['data']
        else:
            add_log(LogStatus.ERROR, LogService.GUI, 'Failed to send a request to the server.')
    except Exception as ex:
        add_log(LogStatus.ERROR, LogService.GUI, ex)
    return False, None


def send_attendance(user_id, date, count):
    user_id = str(user_id)
    date = datetime.strftime(date, "%d.%m.%Y %H:%M:%S")
    return requests.post(attendance_url,
                         json={"token": jewell_token,
                               'user_id': user_id,
                               'date': date,
                               'count': count})


def mp_change_admin_permission(admin_permission):
    return requests.post(admin_permission_url,
                         json={"token": mp_token,
                               'admin_permission': admin_permission})


def mp_reload():
    return requests.post(mp_reload_url,
                         json={"token": mp_token})


def mp_delete_song(song_id):
    return requests.post(delete_song_url,
                         json={"token": mp_token, 'song_id': song_id})


def mp_add_song(song_name, song_author, mp3_file, image_file):
    return requests.post(add_song_url, data={
        'token': mp_token,
        'song_name': song_name,
        'song_author': song_author,
    }, files={
        'mp3_file': (mp3_file.filename, mp3_file.stream, mp3_file.content_type),
        'image_file': (image_file.filename, image_file.stream, image_file.content_type)
    })


def mp_get_admin_permission():
    try:
        r = requests.get(get_admin_permission_url)
        return r.json()['data']
    except:
        return False
