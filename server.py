#!/usr/bin/env python
import sys
import json

from twisted.internet import reactor, ssl
from autobahn.websocket import listenWS
from topchat.api.services import ApiService
from topchat.autobahn.factory import BroadcastServerFactory
from topchat.autobahn.protocol import BroadcastServerProtocol

if __name__ == '__main__':

    if len(sys.argv) == 3 and sys.argv[1] == '-f':
        settings_filename = sys.argv[2]
    elif len(sys.argv) > 1:
        print "Usage: python server.py [-f settings filename]"
        sys.exit()
    else:
        settings_filename = 'dev_settings.json'
        
    try:
        settings_file = open(settings_filename)
        json_settings = json.load(settings_file)
        settings_file.close() 
    except IOError:
        print "The file {0} does not exist".format(settings_filename)
        sys.exit()
        
    contextFactory = ssl.DefaultOpenSSLContextFactory(json_settings['SSL_PRIVATE_KEY'], json_settings['SSL_CERTIFICATE'])
    ServerFactory = BroadcastServerFactory
    api_service = ApiService(json_settings)
    factory = ServerFactory("wss://localhost:{0}".format(json_settings['WEBSOCKET_PORT']), api_service)

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory, contextFactory)

    reactor.run()
