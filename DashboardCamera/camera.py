import os
import sys
import threading
import time
from collections import deque

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import asyncio
import json
from datetime import datetime, timedelta

import cv2
import face_recognition
import websockets
from pytz import timezone

from DashboardCamera.MongoDB.logs import add_log
from DashboardCamera.MongoDB.timetables import get_timetable_by_name
from DashboardCamera.MongoDB.users import get_users
from DashboardCamera.api import send_attendance_visit, get_qr_visits_uri, say_text
from DashboardCamera.models.log import LogStatus, LogService
from DashboardCamera.models.user import Role, Reward, Sex
from DashboardCamera.models.visit import VisitType

tz = timezone('Europe/Moscow')
COURSE_TIME = 2  # hours
VISIT_RANGE_MINUTES_30_MIN = 30 * 60  # seconds
VISIT_RANGE_MINUTES_15_MIN = 15 * 60  # seconds
MAX_HANDLING_FACES = 3

# Общая очередь для хранения данных, отправляемых клиентам
data_queue = deque()


def is_shabbat_time(current_time):
    if ((current_time.weekday() == 4 and current_time.hour > 12) or
            (current_time.weekday() == 5 and current_time.hour < 23)):
        return True
    else:
        return False


def get_timetable_message(date):
    res_timetable_message = ''
    r = get_timetable_by_name('jewell')
    if r.success:
        timetable = r.data.days
        for i in timetable[date.weekday()]:
            start_time = date.replace(hour=i['hours'], minute=i['minutes'], second=0)
            if (date < start_time and (start_time - date).seconds < VISIT_RANGE_MINUTES_30_MIN) or (
                    date > start_time and (date - start_time).seconds < VISIT_RANGE_MINUTES_15_MIN):
                seconds_left = ((start_time + timedelta(seconds=VISIT_RANGE_MINUTES_15_MIN)) - date).seconds
                mins = str(seconds_left // 60)
                secs = str(seconds_left % 60)
                timeleft = f'{mins}:{(2 - len(secs)) * "0" + secs}'
                res_timetable_message += f'Приход на {"/".join(i["courses"])}: {timeleft}\n'
            else:
                end_time = start_time + timedelta(hours=COURSE_TIME)
                if (date < end_time and (end_time - date).seconds < VISIT_RANGE_MINUTES_15_MIN) or (
                        date > end_time and (date - end_time).seconds < VISIT_RANGE_MINUTES_30_MIN):
                    seconds_left = ((end_time + timedelta(seconds=VISIT_RANGE_MINUTES_30_MIN)) - date).seconds
                    mins = str(seconds_left // 60)
                    secs = str(seconds_left % 60)
                    timeleft = f'{mins}:{(2 - len(secs)) * "0" + secs}'
                    res_timetable_message += f'Уход с {"/".join(i["courses"])}: {timeleft}\n'
    return res_timetable_message


def recognise_faces():
    last_user = {
        "id": None,
        "date": None
    }
    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened():
        try:
            now = datetime.now(tz)
            if is_shabbat_time(now):
                continue
            ret, frame = video_capture.read()  # take an image from the camera
            if ret:
                encodings = face_recognition.face_encodings(frame)  # find faces in the frame
                for user_encoding in encodings[:MAX_HANDLING_FACES]:
                    for user in get_users().data:
                        if len(user.face_id.encodings) == 0:
                            continue
                        # Compare the face encoding with encodings from the database
                        matching_results = face_recognition.compare_faces(user.face_id.encodings, user_encoding,
                                                                          tolerance=0.5)
                        # Count the number of successful matches
                        successful_matches = sum(matching_results)
                        # Calculate the percentage of successful matches
                        match_percentage = successful_matches / len(user.face_id.encodings)
                        if match_percentage >= 0.5:
                            if last_user['id'] == user.id and (now - last_user['date']).seconds <= 5:
                                continue
                            last_user = {
                                "id": user.id,
                                "date": now
                            }

                            if get_timetable_message(now):
                                if user.role == Role.STUDENT and user.reward != Reward.NULL:
                                    try:
                                        resp = send_attendance_visit(user.id, now)
                                        if resp.ok:
                                            res = resp.json()
                                            if res['success']:
                                                visit_res = res['data']
                                                visit_msg = ''
                                                if visit_res['visit_type'] == VisitType.ENTER.value:
                                                    visit_msg = f"{user.first_name} {'пришла' if user.sex == Sex.FEMALE else 'пришел'} на занятие {'/'.join(visit_res['courses'])}"
                                                elif visit_res['visit_type'] == VisitType.EXIT.value:
                                                    visit_msg = f"{user.first_name} {'ушла' if user.sex == Sex.FEMALE else 'ушел'} c занятия {'/'.join(visit_res['courses'])}"
                                                data_queue.appendleft({'region': 'center',
                                                                       'message': visit_msg})
                                            else:
                                                visit_msg = res['data']
                                                if visit_msg:
                                                    data_queue.appendleft({'region': 'center',
                                                                           'message': visit_msg})
                                        else:
                                            add_log(LogStatus.ERROR, LogService.CAMERA,
                                                    f'Не удалось отправить запрос на отметку посещаемости: {user.phone_number}')
                                    except Exception as ex:
                                        add_log(LogStatus.ERROR, LogService.CAMERA, ex)

                            message = f'{user.face_id.greeting}, {user.first_name}!\n'
                            data_queue.appendleft({'region': 'bottom_center', 'message': message})
                            say_text(message)

                            break
        except Exception as ex:
            print(ex)
            # add_log(LogStatus.ERROR, LogService.CAMERA, ex)


def display_courses_qr_code():
    last_qr_code_timestamp = datetime.now(tz)
    while True:
        try:
            now = datetime.now(tz)
            if is_shabbat_time(now):
                continue
            if get_timetable_message(now):
                if (now - last_qr_code_timestamp).seconds > 12:
                    uri = get_qr_visits_uri()
                    if uri:
                        last_qr_code_timestamp = now
                        data_queue.appendleft({'region': 'qr_code', 'message': uri})
                        time.sleep(1)
        except Exception as ex:
            print(ex)
            # add_log(LogStatus.ERROR, LogService.CAMERA, ex)


def display_timetable():
    last_timetable_message_flag = False
    timetable_message = ''
    while True:
        try:
            now = datetime.now(tz)
            if is_shabbat_time(now):
                continue

            timetable_message = get_timetable_message(now)
            if timetable_message:
                last_timetable_message_flag = True
                data_queue.append({'region': 'bottom_left', 'message': timetable_message})
            elif last_timetable_message_flag:
                last_timetable_message_flag = False
                data_queue.append({'region': 'bottom_left', 'message': ''})
                data_queue.append({'region': 'qr_code', 'message': ''})
            time.sleep(0.5)
        except Exception as ex:
            # print(ex)
            add_log(LogStatus.ERROR, LogService.CAMERA, ex)


async def sockets_producer(websocket, path):
    while True:
        try:
            # Получаем данные из общей очереди
            if data_queue:
                data = data_queue.popleft()
                await websocket.send(json.dumps(data))
                await asyncio.sleep(0.25)
        except Exception as ex:
            add_log(LogStatus.ERROR, LogService.CAMERA, ex)


if __name__ == "__main__":
    # Создаем отдельные потоки для каждой функции
    timetable_thread = threading.Thread(target=display_timetable)
    qr_code_thread = threading.Thread(target=display_courses_qr_code)
    faces_thread = threading.Thread(target=recognise_faces)

    # Запускаем потоки
    timetable_thread.start()
    qr_code_thread.start()
    faces_thread.start()

    # Запускаем WebSocket-сервер в основном потоке
    server = websockets.serve(sockets_producer, "localhost", 8080)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

    add_log(LogStatus.ERROR, LogService.CAMERA, 'CAMERA service stopped.')
