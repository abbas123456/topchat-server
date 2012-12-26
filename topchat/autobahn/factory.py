import json

from autobahn.websocket import WebSocketServerFactory
from topchat.api import messages
from topchat.client.manager import UserManager, RoomManager
from topchat.api.messages import UserMessage


class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, api_service, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.rooms = {}
        self.api_service = api_service

    def handle_new_request(self, websocket):
        print "Received connection on {0}".format(websocket.http_request_path)
        url_chunks = websocket.http_request_path.split('/')[1:] 
        room = self.get_or_create_room(url_chunks[0])
        if len(url_chunks) > 1:
            user = UserManager(self.api_service).create_authenticated_user(websocket, room, url_chunks[1])
        else:
            user = UserManager(self.api_service).create_anonymous_user(websocket, room)
        print "Added user {0} to room {1}".format(user.username, room.name)
        self.initialise_user_list(room, user)
        RoomManager(self.api_service).add_user(room, user)
        self.broadcast_bot_welcome_message(user)
        return user

    def handle_request_end(self, websocket):
        RoomManager(self.api_service).remove_user(websocket.user.room, websocket.user)
        self.broadcast_user_left_message(websocket.user)
        print "Removed user {0} from room {1}".format(websocket.user.username, websocket.user.room.name)

    def handle_message(self, websocket, message):
        message = json.loads(message)
        if message['type'] == 1:
            print "User {0} sent a message in room {1}".format(websocket.user.username, websocket.user.room.name)
            user_message = UserMessage(websocket.user.username, websocket.user.colour_rgb, message['text'])
            self.broadcast(user_message, websocket.user.room)
        elif message['type'] == 2:
            print "User {0} sent a private message to {1}".format(websocket.user.username, message['recipient_username'])
            self.send_private_message(websocket.user, message['recipient_username'], message['text'])

    def broadcast(self, message, room):
        for user in room.users:
            user.websocket.send_direct_message(message)

    def get_or_create_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        else:
            room = RoomManager(self.api_service).create_room(room_id)
            print "Created room {0}".format(room.name)
            self.rooms[room_id] = room
            return room

    def initialise_user_list(self, room, user):
        for current_client in room.users:
            user_joined_message = messages.UserJoinedMessage(current_client.username, current_client.colour_rgb)
            user.websocket.send_direct_message(user_joined_message)

    def broadcast_bot_welcome_message(self, user):
        bot_message = messages.BotMessage("{0} has joined the room".format(user.username))
        self.broadcast(bot_message, user.room)
        user_joined_message = messages.UserJoinedMessage(user.username,user. colour_rgb)
        self.broadcast(user_joined_message, user.room)

    def broadcast_user_left_message(self, user):
        bot_message = messages.BotMessage("{0} has left the room".format(user.username))
        self.broadcast(bot_message, user.room)
        user_left_message = messages.UserLeftMessage(user.username)
        self.broadcast(user_left_message, user.room)

    def send_private_message(self, user, recipient_username, message_text):
        recipient = user.room.get_user_by_username(recipient_username)
        if recipient is not None:
            private_conversation_receive_user_message = messages.PrivateConversationReceiveUserMessage(
                                                       user.username, user.colour_rgb, message_text)
            recipient.websocket.send_direct_message(private_conversation_receive_user_message)

            private_conversation_send_user_message = messages.PrivateConversationSendUserMessage(
                    user.username, user.colour_rgb, message_text, recipient_username)
            user.websocket.send_direct_message(private_conversation_send_user_message)

        else:
            private_bot_message = messages.PrivateBotMessage("Your message could not be sent to {0}, "
            "perhaps they have left the room, or changed their username".format(
                                        recipient_username), recipient_username)
            user.websocket.send_direct_message(private_bot_message)