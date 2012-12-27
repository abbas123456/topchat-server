import json
import sys
import aiml
import os.path

from twisted.internet import reactor
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

if __name__ == '__main__':
    """
    Usage: python client.py [room_id] [settings_filename]"
    """
    if len(sys.argv) == 3:
        settings_filename = sys.argv[2]
        room_id = sys.argv[1]
    elif len(sys.argv) == 2:
        settings_filename = 'dev_settings.json'
        room_id = sys.argv[1]
    else:
        settings_filename = 'dev_settings.json'
        room_id = 1
    try:
        settings_file = open(settings_filename)
        json_settings = json.load(settings_file)
        settings_file.close() 
    except IOError:
        print "The file {0} does not exist".format(settings_filename)
        sys.exit()
    
    kernel = aiml.Kernel()
    if os.path.isfile("standard.brn"):
        kernel.bootstrap(brainFile = "pyaiml/standard.brn")
    else:
        kernel.bootstrap(learnFiles = "pyaiml/std-startup.xml", commands = "load aiml b")
        kernel.saveBrain("pyaiml/standard.brn")
    
    factory = WebSocketClientFactory('ws://localhost:{0}/{1}/{2}'.format(json_settings['WEBSOCKET_PORT'], room_id, json_settings['BOT_TOKEN']))
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)
    reactor.run()
    