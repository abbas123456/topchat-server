import re
import random
import json

from autobahn.websocket import WebSocketServerProtocol, WebSocketProtocol
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

    def onMessage(self, message_text, binary):
        if not binary:
            match = re.match("!CU ([^\s-]+)", message_text, re.IGNORECASE)
            if match is not None:
                new_username = match.groups()[0]
                self.factory.change_username_temporarily(self, new_username)
                return
            
            match = re.match("!RL ([^\s-]+) ([^\s-]+)", message_text, re.IGNORECASE)
            if match is not None:
                username = match.groups()[0]
                password = match.groups()[1]
                self.factory.register_or_login(self, username, password)
                return
            
            match = re.match("<([^\s-]+)>(.*)", message_text)
            if match is not None:
                recipient_username = match.groups()[0]
                message_text = match.groups()[1]
                self.factory.send_private_message(self, recipient_username, message_text)
                return
            
            user_message = UserMessage(self.username, self.colour_rgb, message_text)
            self.factory.broadcast(user_message, self.room_number)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.leave_room(self)

    def send_direct_message(self, message):
        message_json_string = json.dumps(message, cls=MessageEncoder) 
        BroadcastServerProtocol.sendMessage(self, message_json_string)
