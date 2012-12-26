import json
import sys
import pycurl
import cStringIO

from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory,WebSocketClientProtocol,connectWS
import aiml
import os.path

class BroadcastClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.sendMessage(json.dumps({'type':1, 'text': 'Hi all, private conversations only please.'}))

    def onMessage(self, message, binary):
        message = json.loads(message)
        if message['type'] == 7:
            message_text = message['message']
            response = k.respond(message_text, message['username']);
            self.sendMessage(json.dumps({'type':2, 'text': response, 'recipient_username': message['username']}))


if __name__ == '__main__':
    """
    Usage: python client.py [room_id] [settings_filename]"
    """
    if len(sys.argv) == 3:
        settings_filename = sys.argv[2]
        room_id = sys.argv[1]
    elif len(sys.argv) == 2:
        settings_filename = '../dev_settings.json'
        room_id = sys.argv[1]
    else:
        settings_filename = '../dev_settings.json'
        room_id = 1

    try:
        settings_file = open(settings_filename)
        json_settings = json.load(settings_file)
        settings_file.close() 
    except IOError:
        print "The file {0} does not exist".format(settings_filename)
        sys.exit()
        
    k = aiml.Kernel()
    if os.path.isfile("standard.brn"):
        k.bootstrap(brainFile = "standard.brn")
    else:
        k.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
        k.saveBrain("standard.brn")
    
    factory = WebSocketClientFactory('ws://localhost:7000/{0}/{1}'.format(room_id, json_settings['BOT_TOKEN']))
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)

    reactor.run()

    