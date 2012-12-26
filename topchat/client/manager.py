import re
import models


from topchat.client.models import Room

class Manager(object):

    def __init__(self, api_service):
        self.api_service = api_service


class UserManager(Manager):

    def create_anonymous_user(self, websocket, room):
        username = "Guest{0}".format(re.search(':(.*)', websocket.peerstr).groups()[0])
        return models.AnonymousUser(username, websocket, room)

    def create_authenticated_user(self, websocket, room, token_string):
        user_dict = self.api_service.get_user_by_token(token_string)
        if user_dict is None or room.get_user_by_username(user_dict['username']):
            return self.create_anonymous_user(websocket, room)
        else:
            administrated_rooms = [administrated_room['room'] for administrated_room in user_dict['administrated_rooms']]
            return models.AuthenticatedUser(user_dict['username'], websocket, room, room.id in administrated_rooms)


class RoomManager(Manager):

    def add_user(self, room, user):
        room.users.append(user)

    def remove_user(self, room, user):
        room.users.remove(user)

    def ban_user(self, room, user):
        pass

    def unban_user(self, room, user):
        pass
    
    def create_room(self, room_id):
        room_dict = self.api_service.get_room_by_room_number(room_id)
        if room_dict is None:
            return None
        else:
            return Room(room_dict['id'], room_dict['name'])
