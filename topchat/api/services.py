import pycurl
import cStringIO
import json

class CurlService(object):
    
    def __init__(self, settings):
        self.settings = settings
    
    def get_http_response(self, relative_url):
        buffer = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "{0}{1}".format(self.settings['APPLICATION_URL_HOSTNAME'], relative_url))
        curl.setopt(pycurl.USERPWD, "{0}:{1}".format(self.settings['API_USERNAME'], self.settings['API_PASSWORD']))
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.perform()
        response = buffer.getvalue()
        buffer.close()
        return response
        
    def get_https_response(self, relative_url):
        buffer = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "{0}{1}".format(self.settings['APPLICATION_URL_HOSTNAME'], relative_url))
        curl.setopt(pycurl.SSL_VERIFYPEER, self.settings['SSL_VERIFY_PEER'])
        curl.setopt(pycurl.SSL_VERIFYHOST, self.settings['SSL_VERIFY_HOST'])
        curl.setopt(pycurl.CAINFO, str(self.settings['SSL_CERTIFICATE']))
        curl.setopt(pycurl.USERPWD, "{0}:{1}".format(self.settings['API_USERNAME'], self.settings['API_PASSWORD']))
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.perform()
        response = buffer.getvalue()
        buffer.close()
        return response
    
    def http_post(self, relative_url, postfields):
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "{0}{1}".format(self.settings['APPLICATION_URL_HOSTNAME'], relative_url))
        curl.setopt(pycurl.POSTFIELDS, postfields)
        curl.setopt(pycurl.USERPWD, "{0}:{1}".format(self.settings['API_USERNAME'], self.settings['API_PASSWORD']))
        curl.perform()
    
    def https_post(self, relative_url, postfields):    
        buffer = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "{0}{1}".format(self.settings['APPLICATION_URL_HOSTNAME'], relative_url))
        curl.setopt(pycurl.POSTFIELDS, postfields)
        curl.setopt(pycurl.SSL_VERIFYPEER, self.settings['SSL_VERIFY_PEER'])
        curl.setopt(pycurl.SSL_VERIFYHOST, self.settings['SSL_VERIFY_HOST'])
        curl.setopt(pycurl.CAINFO, str(self.settings['SSL_CERTIFICATE']))
        curl.setopt(pycurl.USERPWD, "{0}:{1}".format(self.settings['API_USERNAME'], self.settings['API_PASSWORD']))
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.perform()
        response = buffer.getvalue()
        buffer.close()
        return response

    def http_delete(self, relative_url):    
        curl = pycurl.Curl()
        curl.setopt(curl.URL, "{0}{1}".format(self.settings['APPLICATION_URL_HOSTNAME'], relative_url))
        curl.setopt(pycurl.POSTFIELDS, "_method=DELETE")
        curl.setopt(pycurl.USERPWD, "{0}:{1}".format(self.settings['API_USERNAME'], self.settings['API_PASSWORD']))
        curl.perform()


class ApiService(object):
    
    PERSISTENT_USERNAMES = ['mobot']

    def __init__(self, settings):        
        self.curl_service = CurlService(settings)

    def get_all_rooms(self):
        relative_url = "rooms/.json"
        rooms = json.loads(self.curl_service.get_http_response(relative_url))
        return rooms or {}

    def get_room_by_room_number(self, room_number):
        relative_url = "rooms/{0}/.json".format(room_number)
        room = json.loads(self.curl_service.get_http_response(relative_url))
        if 'id' in room and room['is_active']:
            return room
        else:
            return None

    def get_user_by_token(self, token_string):
        relative_url = "user-tokens/{0}/.json".format(token_string)
        user = json.loads(self.curl_service.get_http_response(relative_url))
        relative_url = "delete-user-token/{0}/".format(token_string)
        if user['user']['username'] not in self.PERSISTENT_USERNAMES:
            self.curl_service.http_delete(relative_url)
        if 'user' in user:
            return user['user']
        else:
            return None

    def ban_user_from_room(self, user):
        relative_url = "banned-users/"
        self.curl_service.http_post(relative_url, "banned_user={0}&room={1}".format(user.id, user.room.id))