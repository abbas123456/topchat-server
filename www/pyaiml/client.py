import json
import sys
import aiml
import os.path

from twisted.internet import reactor, ssl
from autobahn.websocket import WebSocketClientFactory,WebSocketClientProtocol,connectWS


class BroadcastClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.sendMessage(json.dumps({'type':1, 'text': 'Hi all, private conversations only please.'}))

    def onMessage(self, message, binary):
        message = json.loads(message)
        if message['type'] == 7:
            message_text = message['message']
            response = kernel.respond(message_text, message['username']);
            self.sendMessage(json.dumps({'type':2, 'text': response, 'recipient_username': message['username']}))

    def onClose(self, wasClean, code, reason):
        connectWS(factory, ssl.ClientContextFactory())

if __name__ == '__main__':
    """
    Usage: python client.py [room_id] [environment]"
    """
    if len(sys.argv) == 3:
        environment = sys.argv[2]
        room_id = sys.argv[1]
    elif len(sys.argv) == 2:
        environment = 'local'
        room_id = sys.argv[1]
    else:
        environment = 'local'
        room_id = 1
    try:
        settings_file = open("../settings/{0}.conf".format(environment))
        json_settings = json.load(settings_file)
        settings_file.close() 
    except IOError:
        print "The file {0}.conf does not exist".format(environment)
        sys.exit()
    
    kernel = aiml.Kernel()
    if os.path.isfile("standard.brn"):
        kernel.bootstrap(brainFile = "standard.brn")
    else:
        kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
        kernel.saveBrain("standard.brn")
    
    factory = WebSocketClientFactory("{0}://{1}:{2}/{3}/{4}".format(json_settings['WEBSOCKET_SCHEME'],
                                     json_settings['WEBSOCKET_DOMAIN'],
                                     json_settings['WEBSOCKET_PORT'],
                                     room_id,
                                     json_settings['BOT_TOKEN']))
    factory.protocol = BroadcastClientProtocol
    connectWS(factory, ssl.ClientContextFactory())
    reactor.run()
    