import random


class User(object):

    def __init__(self, username, websocket, room, is_administrator, id=None):
        self.id = id
        self.colour_rgb = [random.randint(0, 255) for x in range(3)]
        self.username = username
        self.websocket = websocket
        self.room = room
        self.is_administrator = is_administrator

class AnonymousUser(User):
    def __init__(self, username, websocket, room):
        super(AnonymousUser, self).__init__(username, websocket, room, False)


class AuthenticatedUser(User):
    
    def __init__(self, username, websocket, room, is_administrator, id):
        super(AuthenticatedUser, self).__init__(username, websocket, room, is_administrator, id)


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
