import json

from autobahn.websocket import WebSocketServerProtocol
from topchat.api.messages import MessageEncoder


class WebSocket(WebSocketServerProtocol):

    def onOpen(self):
        self.user = self.factory.handle_new_request(self)

    def onMessage(self, message, binary):
        if not binary:
            self.factory.handle_message(self, message)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.handle_request_end(self)

    def disconnect(self):
        WebSocketServerProtocol.dropConnection(self, abort=True)
        
    def send_direct_message(self, message):
        message_json_string = json.dumps(message, cls=MessageEncoder) 
        WebSocket.sendMessage(self, message_json_string)
