import asyncio
from datetime import datetime
from pytz import timezone

import cv2
import face_recognition
import websockets

from DashboardCamera.MongoDB.timetables import get_timetable_by_name
from DashboardCamera.MongoDB.users import get_users
from DashboardCamera.MongoDB.visits import get_visits_by_user_id, add_visit
from DashboardCamera.models.user import Role, Reward

tz = timezone('Europe/Moscow')


async def recognise_faces(websocket, path):
    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened():
        ret, frame = video_capture.read()  # take image from camera
        if ret:
            encodings = face_recognition.face_encodings(frame)  # find faces in frame
            if len(encodings) > 0:
                user_encoding = encodings[0]
                for user in get_users().data:
                    results = face_recognition.compare_faces(user.encodings, user_encoding)
                    if any(results):
                        message = f'Привет, {user.first_name}'
                        if user.role == Role.STUDENT and user.reward != Reward.NULL:
                            now = datetime.now(tz)
                            r = get_timetable_by_name('jewell')
                            if r.success:
                                timetable = r.data.days
                                visits = get_visits_by_user_id(user.id).data
                                for i in timetable[now.weekday()]:
                                    if len(visits) % 2 == 0:
                                        start_time = now.replace(hour=i['hours'], minute=i['minutes'])
                                        if (now < start_time and (start_time - now).seconds < 15 * 60) or (
                                                now > start_time and (now - start_time).seconds < 15 * 60):
                                            add_visit(user.id, now)
                                            message = f"пришел на занятие {i['courses']}"
                                            break
                                    else:
                                        end_time = now.replace(hour=i['hours'] + 2, minute=i['minutes'])
                                        if (now < end_time and (end_time - now).seconds < 15 * 60) or (
                                                now > end_time and (now - end_time).seconds < 15 * 60):
                                            add_visit(user.id, now)
                                            message = f"ушел с занятия {i['courses']}"
                                            break
                        await websocket.send(message)  # todo beauty messages
                        await asyncio.sleep(1)
                        break


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
# todo inform admins in tg or request to site that camera stopped
