#!/usr/bin/env python
import sys
import json
import os

from twisted.internet import reactor, ssl
from autobahn.websocket import listenWS
from topchat.api.services import ApiService
from topchat.autobahn.factory import BroadcastServerFactory
from topchat.autobahn.protocol import WebSocket

if __name__ == '__main__':

    if len(sys.argv) == 2:
        environment = sys.argv[1]
    elif len(sys.argv) > 1:
        print "Usage: python server.py [environment]"
        sys.exit()
    else:
        environment = 'local'
    
    os.environ['environment'] = environment
        
    try:
        settings_file = open("settings/{0}.conf".format(environment))
        json_settings = json.load(settings_file)
        settings_file.close() 
    except IOError:
        print "The file {0}.conf does not exist".format(environment)
        sys.exit()
     
    api_service = ApiService(json_settings)
    factory = BroadcastServerFactory("{0}://{1}:{2}".format(json_settings['WEBSOCKET_SCHEME'],
                                     json_settings['WEBSOCKET_DOMAIN'],
                                     json_settings['WEBSOCKET_PORT']), api_service)

    factory.protocol = WebSocket
    factory.setProtocolOptions(allowHixie76=True)
    
    contextFactory = ssl.DefaultOpenSSLContextFactory(json_settings['SSL_PRIVATE_KEY'], json_settings['SSL_CERTIFICATE'])
    listenWS(factory, contextFactory)
    
    reactor.run()
