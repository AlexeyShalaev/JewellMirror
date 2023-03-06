import asyncio
import random
from datetime import datetime, timedelta
from pytz import timezone

import cv2
# import face_recognition
import websockets

from DashboardCamera.MongoDB.timetables import get_timetable_by_name
from DashboardCamera.MongoDB.users import get_users
from DashboardCamera.MongoDB.visits import get_visits_by_user_id, add_visit
from DashboardCamera.models.user import Role, Reward
from DashboardCamera.models.visit import VisitType

tz = timezone('Europe/Moscow')


async def recognise_faces(websocket, path):
    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened():
        ret, frame = video_capture.read()  # take image from camera
        if ret:
            encodings = [1]  # develop
            # encodings = face_recognition.face_encodings(frame)  # find faces in frame
            if len(encodings) > 0:
                user_encoding = encodings[0]
                for user in get_users().data:
                    # results = face_recognition.compare_faces(user.encodings, user_encoding)
                    results = [random.choice([True, False])]  # develop
                    if any(results):
                        message = f'Шалом, {user.first_name}!\n'
                        if user.role == Role.STUDENT and user.reward != Reward.NULL:
                            now = datetime.now(tz)
                            r = get_timetable_by_name('jewell')
                            if r.success:
                                timetable = r.data.days
                                visits = [visit for visit in get_visits_by_user_id(user.id).data if
                                          (now - visit.date).seconds < 24 * 60 * 60]
                                visits.sort(key=lambda x: x.date, reverse=True)
                                for i in timetable[now.weekday()]:
                                    start_time = now.replace(hour=i['hours'], minute=i['minutes'])
                                    if len(visits) == 0 or visits[0].visit_type == VisitType.EXIT:
                                        if (now < start_time and (start_time - now).seconds < 15 * 60) or (
                                                now > start_time and (now - start_time).seconds < 15 * 60):
                                            add_visit(user.id, now, VisitType.ENTER, i['courses'])
                                            message += f"Ты пришел(-ла) на занятие {'/'.join(i['courses'])}"
                                            break
                                    else:
                                        if visits[0].courses == i['courses']:
                                            end_time = start_time + timedelta(hours=2)
                                            if (now < end_time and (end_time - now).seconds < 15 * 60) or (
                                                    now > end_time and (now - end_time).seconds < 15 * 60):
                                                add_visit(user.id, now, VisitType.EXIT, i['courses'])
                                                message += f"Ты ушел(-ла) с занятия {'/'.join(i['courses'])}"
                                                break
                        await websocket.send(message)
                        await asyncio.sleep(1)
                        break


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
# todo inform admins in tg or request to site that camera stopped
# todo display on mirror осталось мин до окончания отмечания на начало/конец для тех или иных курсов
