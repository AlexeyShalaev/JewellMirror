import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DashboardCamera.speech import say

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
from DashboardCamera.api import send_attendance_visit, get_qr_visits_uri
from DashboardCamera.models.log import LogStatus, LogService
from DashboardCamera.models.user import Role, Reward, Sex
from DashboardCamera.models.visit import VisitType

tz = timezone('Europe/Moscow')
ONE_DAY = 24 * 60 * 60  # seconds
COURSE_TIME = 2  # hours
VISIT_RANGE_MINUTES = 15  # minutes
VISIT_RANGE_SECONDS = VISIT_RANGE_MINUTES * 60  # seconds
MAX_HANDLING_FACES = 3


def is_shabbat_time(current_time):
    if ((current_time.weekday() == 4 and current_time.hour > 12) or
            (current_time.weekday() == 5 and current_time.hour < 23)):
        return True
    else:
        return False


async def recognise_faces(websocket, path):
    video_capture = cv2.VideoCapture(0)
    last_user = {
        "id": None,
        "date": None
    }
    last_qr_code_timestamp = datetime.now(tz)
    last_timetable_message_flag = False
    while video_capture.isOpened():
        try:
            now = datetime.now(tz)

            if is_shabbat_time(now):
                continue

            r = get_timetable_by_name('jewell')
            if r.success:
                timetable = r.data.days
                timetable_message = ''
                for i in timetable[now.weekday()]:
                    start_time = now.replace(hour=i['hours'], minute=i['minutes'], second=0)
                    if (now < start_time and (start_time - now).seconds < VISIT_RANGE_SECONDS) or (
                            now > start_time and (now - start_time).seconds < VISIT_RANGE_SECONDS):
                        seconds_left = ((start_time + timedelta(minutes=VISIT_RANGE_MINUTES)) - now).seconds
                        mins = str(seconds_left // 60)
                        secs = str(seconds_left % 60)
                        timeleft = f'{mins}:{(2 - len(secs)) * "0" + secs}'
                        timetable_message += f'До окончания прихода на {"/".join(i["courses"])}: {timeleft}\n'
                    else:
                        end_time = start_time + timedelta(hours=COURSE_TIME)
                        if (now < end_time and (end_time - now).seconds < VISIT_RANGE_SECONDS) or (
                                now > end_time and (now - end_time).seconds < VISIT_RANGE_SECONDS):
                            seconds_left = ((end_time + timedelta(minutes=VISIT_RANGE_MINUTES)) - now).seconds
                            mins = str(seconds_left // 60)
                            secs = str(seconds_left % 60)
                            timeleft = f'{mins}:{(2 - len(secs)) * "0" + secs}'
                            timetable_message += f'До окончания ухода с {"/".join(i["courses"])}: {timeleft}\n'
                if timetable_message != '':
                    last_timetable_message_flag = True
                    await websocket.send(json.dumps({'region': 'bottom_left', 'message': timetable_message}))
                    await asyncio.sleep(0.5)

                    if (now - last_qr_code_timestamp).seconds > 10:
                        uri = get_qr_visits_uri()
                        if uri:
                            last_qr_code_timestamp = now
                            await websocket.send(json.dumps({'region': 'qr_code', 'message': uri}))
                            await asyncio.sleep(0.5)
                elif last_timetable_message_flag:
                    last_timetable_message_flag = False
                    await websocket.send(json.dumps({'region': 'bottom_left', 'message': ''}))
                    await websocket.send(json.dumps({'region': 'qr_code', 'message': ''}))
                    await asyncio.sleep(0.5)
                ret, frame = video_capture.read()  # take image from camera
                if ret:
                    encodings = face_recognition.face_encodings(frame)  # find faces in frame
                    for user_encoding in encodings[:MAX_HANDLING_FACES]:
                        for user in get_users().data:
                            results = face_recognition.compare_faces(user.face_id.encodings, user_encoding,
                                                                     tolerance=0.5)
                            if any(results):
                                if last_user['id'] == user.id and (now - last_user['date']).seconds <= 5:
                                    continue
                                last_user = {
                                    "id": user.id,
                                    "date": now
                                }
                                message = f'{user.face_id.greeting}, {user.first_name}!\n'
                                await websocket.send(json.dumps({'region': 'bottom_center', 'message': message}))
                                await asyncio.sleep(0.5)
                                say(message)

                                if user.role == Role.STUDENT and user.reward != Reward.NULL:
                                    resp = send_attendance_visit(user.id, now)
                                    if resp.ok:
                                        res = resp.json()
                                        if res['success']:
                                            messages = res['data']
                                            if messages:
                                                visit_msg = ''
                                                for i in messages:
                                                    if i['visit_type'] == VisitType.ENTER.value:
                                                        visit_msg += f"{user.first_name} {'пришла' if user.sex == Sex.FEMALE else 'пришел'} на занятие {'/'.join(i['courses'])}"
                                                    elif i['visit_type'] == VisitType.EXIT.value:
                                                        visit_msg += f"{user.first_name} {'ушла' if user.sex == Sex.FEMALE else 'ушел'} на занятие {'/'.join(i['courses'])}"
                                                    visit_msg += '\n'

                                                await websocket.send(json.dumps({'region': 'center',
                                                                                 'message': visit_msg}))
                                                await asyncio.sleep(1)
                                                say(visit_msg)

                                break
        except Exception as ex:
            # add_log(LogStatus.ERROR, LogService.CAMERA, ex)
            await asyncio.sleep(1)


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

add_log(LogStatus.ERROR, LogService.CAMERA, 'CAMERA service stopped.')
