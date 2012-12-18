import re
import random
import json

from autobahn.websocket import WebSocketServerProtocol
from objects import UserMessage, MessageEncoder

class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.colour_rgb = [random.randint(0, 255) for x in range(3)]
        matches = re.match(r"\/(\d+)", self.http_request_path)
        self.room_number = 1 if matches is None else matches.group(1)
        matches = re.match(r".*\/(.*)\/(.*)$", self.http_request_path)
        if not matches is None:
            self.username = matches.group(1)
            self.encrypted_password = matches.group(2)
        else:
            self.username = "Guest{0}".format(re.search(':(.*)', self.peerstr).groups()[0])
        
        self.factory.join_room(self)

    def onMessage(self, message, binary):
        if not binary:
            message = json.loads(message)
            if message['type'] == 1:
                user_message = UserMessage(self.username, self.colour_rgb, message['text'])
                self.factory.broadcast(user_message, self.room_number)
            elif message['type'] == 2:
                self.factory.change_username_temporarily(self, message['username'])
            elif message['type'] == 3:
                self.factory.register_or_login(self, message['username'], message['password'])
            elif message['type'] == 4:
                self.factory.send_private_message(self, message['recipient_username'], message['text'])

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.leave_room(self)

    def send_direct_message(self, message):
        message_json_string = json.dumps(message, cls=MessageEncoder) 
        BroadcastServerProtocol.sendMessage(self, message_json_string)
