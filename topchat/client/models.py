import random


class User(object):

    def __init__(self, username, websocket, room):
        self.colour_rgb = [random.randint(0, 255) for x in range(3)]
        self.username = username
        self.websocket = websocket
        self.room = room


class AnonymousUser(User):
    pass


class AuthenticatedUser(User):
    pass


class Room(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.users = []

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
