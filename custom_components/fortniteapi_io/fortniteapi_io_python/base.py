import json

import furl
import requests

from .exceptions import UnauthorizedError, NotFoundError, UnknownPlayerError
from .domain import Mode, Languages, Input, Player


class FortniteAPI_IO:
    """The Fortnite class provides access to fortniteapi.io's API endpoints"""

    def __init__(self, api_key):
        self.client = Client(api_key)
    
    # def search_id

    def player(self, account_id=None, language=Languages.DE):
        """Player endpoint"""
        endpoint = 'stats?account=%s' % (account_id)
        data = self.client.request(endpoint)
        if data.get("result") == True:
            return Player(data)
        raise UnknownPlayerError
    
    def get_current_map(self, poi=True):
        """Map endpoint"""
        poi_attr = "%s" % (poi)
        return "https://media.fortniteapi.io/images/map.png?showPOI=%s" % (poi_attr.lower())
    
    def get_account_id(self, username=None):
        """Search Account ID endpoint"""
        endpoint = 'lookup?username=%s' % (username)
        data = self.client.request(endpoint)
        if data.get("result") == True:
            return data.get("account_id")
        raise UnknownPlayerError

class Client:
    """The Client class is a wrapper around the requests library"""

    BASE_URL    = 'https://fortniteapi.io/v1/'
    BASE_URL_V2 = 'https://fortniteapi.io/v2/'

    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
        })
        self.url = furl.furl(self.BASE_URL)

    API_OK = 200
    API_ERRORS_MAPPING = {
        401: UnauthorizedError,
        400: NotFoundError,
        403: UnauthorizedError,
    }

    def request(self, endpoint, version=1):
        """This function does the request to the api with the endpoint
        provided and returns de json (if the response is ok)"""
        if version == 1:
            response = self.session.get(self.BASE_URL + endpoint)
        else:
            response = self.session.get(self.BASE_URL_V2 + endpoint)
        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, Exception)
            raise exception

        return json.loads(response.text)
