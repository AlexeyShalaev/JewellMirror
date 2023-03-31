import asyncio
import json
from datetime import datetime, timedelta

import cv2
import face_recognition
import websockets
from pytz import timezone

from MongoDB.logs import add_log
from MongoDB.timetables import get_timetable_by_name
from MongoDB.users import get_users
from MongoDB.visits import get_visits_by_user_id, add_visit
from api import update_user_attendance
from models.log import LogStatus, LogService
from models.user import Role, Reward
from models.visit import VisitType

tz = timezone('Europe/Moscow')
ONE_DAY = 24 * 60 * 60  # seconds
COURSE_TIME = 2  # hours
VISIT_RANGE_MINUTES = 15  # minutes
VISIT_RANGE_SECONDS = VISIT_RANGE_MINUTES * 60  # seconds


async def recognise_faces(websocket, path):
    video_capture = cv2.VideoCapture(0)
    last_user = {
        "id": None,
        "date": None
    }
    while video_capture.isOpened():
        try:
            now = datetime.now(tz)
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
                    await websocket.send(json.dumps({'region': 'bottom_left', 'message': timetable_message}))
                    await asyncio.sleep(0.5)
                ret, frame = video_capture.read()  # take image from camera
                if ret:
                    encodings = face_recognition.face_encodings(frame)  # find faces in frame
                    if len(encodings) > 0:
                        user_encoding = encodings[0]
                        for user in get_users().data:
                            results = face_recognition.compare_faces(user.encodings, user_encoding)
                            if any(results):
                                if last_user['id'] == user.id and (now - last_user['date']).seconds <= 5:
                                    continue
                                last_user = {
                                    "id": user.id,
                                    "date": now
                                }
                                message = f'Шалом, {user.first_name}!\n'
                                if user.role == Role.STUDENT and user.reward != Reward.NULL:
                                    visits = [visit
                                              for visit in get_visits_by_user_id(user.id).data
                                              if (now - visit.date).seconds < ONE_DAY
                                              and now.weekday() == visit.date.weekday()]
                                    visits.sort(key=lambda x: x.date, reverse=True)
                                    for i in timetable[now.weekday()]:
                                        start_time = now.replace(hour=i['hours'], minute=i['minutes'])
                                        if len(visits) == 0 or visits[0].visit_type == VisitType.EXIT:
                                            if (now < start_time and (
                                                    start_time - now).seconds < VISIT_RANGE_SECONDS) or (
                                                    now > start_time and (
                                                    now - start_time).seconds < VISIT_RANGE_SECONDS):
                                                add_visit(user.id, now, VisitType.ENTER, i['courses'])
                                                await websocket.send(json.dumps({'region': 'center',
                                                                                 'message': f"{user.first_name} пришел(-ла) на занятие {'/'.join(i['courses'])}"}))
                                                await asyncio.sleep(1)
                                                break
                                        else:
                                            if visits[0].courses == i['courses']:
                                                end_time = start_time + timedelta(hours=COURSE_TIME)
                                                if (now < end_time and (
                                                        end_time - now).seconds < VISIT_RANGE_SECONDS) or (
                                                        now > end_time and (
                                                        now - end_time).seconds < VISIT_RANGE_SECONDS):
                                                    add_visit(user.id, now, VisitType.EXIT, i['courses'])
                                                    await update_user_attendance(user.id, now, 1)
                                                    await websocket.send(json.dumps({'region': 'center',
                                                                                     'message': f"Ты ушел(-ла) с занятия {'/'.join(i['courses'])}"}))
                                                    await asyncio.sleep(1)
                                                    break
                                await websocket.send(json.dumps({'region': 'bottom_center', 'message': message}))
                                await asyncio.sleep(1)
                                break
        except Exception as ex:
            add_log(LogStatus.ERROR, LogService.CAMERA, ex)
            await asyncio.sleep(1)


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

add_log(LogStatus.ERROR, LogService.CAMERA, 'CAMERA service stopped.')
