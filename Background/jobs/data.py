from datetime import datetime, timedelta

from Background.MongoDB.users import get_users


def manage_data():
    pass
    # get all faces
    # filter only students with reward not null
    # send to api while answer not true else telegram warning
    # clear faces
    # update data from jms (users)
    update_users()
    update_courses()


def update_users():
    # обновляем данные о поль-ах, чтобы вдруг кто-тьо обновил фото лица
    pass


def update_courses():
    # обновляем данные о курсах, чтобы понимать по времени какой сейчас ближ. курс
    pass
