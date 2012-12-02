import pycurl
import cStringIO
import json

class CurlService(object):
    
    def __init__(self, settings):
        self.settings = settings
    
    def get_http_response(self, relative_url):
        buffer = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(c.WRITEFUNCTION, buffer.write)
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

class ApiService(object):
    
    def __init__(self, settings):        
        self.curl_service = CurlService(settings)
        
    def get_room_by_room_number(self, room_number):
        relative_url = "room/{0}/".format(room_number)
        room = json.loads(self.curl_service.get_https_response(relative_url))
        if 'id' in room:
            return room
        else:
            return None
    
    def get_user_by_username(self, username):
        relative_url = "user/{0}/".format(username)
        user = json.loads(self.curl_service.get_https_response(relative_url))
        if 'id' in user:
            return user
        else:
            return None
    
    def get_user_by_username_and_raw_password(self, username, raw_password):
        relative_url = "user/{0}/{1}/".format(username, raw_password)
        user = json.loads(self.curl_service.get_https_response(relative_url))
        if 'id' in user:
            return user
        else:
            return None
        
    def get_user_by_username_and_encrypted_password(self, username, encrypted_password):
        relative_url = "user/{0}/".format(username)
        user = json.loads(self.curl_service.get_https_response(relative_url))
        if 'id' in user and user['password'] == encrypted_password:
            return user
        else:
            return None
    
    def register_user(self, username, raw_password):
        relative_url = "users/"
        postfields = "username={0}&password={1}".format(username, raw_password)
        user = json.loads(self.curl_service.https_post(relative_url, postfields))
        return user
