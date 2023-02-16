import asyncio
from datetime import datetime

import cv2
import face_recognition
import websockets

from DashboardCamera.MongoDB.users import get_users
from DashboardCamera.models.user import Role


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
                        if user.role == Role.STUDENT:
                            now = datetime.now()
                            # todo member that this user was on course
                        message = f'Привет, {user.first_name}'
                        await websocket.send(message)
                        await asyncio.sleep(1)
                        break


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
# todo inform admins in tg or request to site that camera stopped
