from flask_login import UserMixin


class UserLogin(UserMixin):
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name
