import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib.parse
import logging
import json
from util.database import DatabaseConnector as dc

logger = logging.getLogger("django")

class Jira:
    session = None
    u_auth = 'rest/auth/1/session'
    server = None
    def __init__(self, sever=None):
        self.server = sever or 'https://jiradc2.ext.net.nokia.com/'
        db = dc('devicedp')
        df = db.read_query('select `Token` from tbl_api_token limit 1')
        logger.info(f'df = {df}')
        token = df.at[0, "Token"]
        logger.info(f'api token = {token}')
        self._headers = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {token}'
        }
        requests.packages.urllib3.disable_warnings(
            InsecureRequestWarning
        )
        self.session = requests.Session()
        pass

    def get(self, url, params = None):
        u = '{}{}'.format(self.server, url)
        if params:
            u += '?%s' % urllib.parse.urlencode(params) 
        logger.debug('url = %s' % u)
        resp = self.session.get(
            url=u,
            headers=self._headers,
            verify=False
        )
        logger.debug('resp = %s' % resp.text)
        return  resp

    def post(self, url, data):
        resp = self.session.post(
            '{}{}'.format(self.server, url), 
            data=json.dumps(data), 
            headers=self._headers,
            verify = False
        )
        return resp.ok
        pass
        
    def post_with_resp(self, url, data):
        resp = self.session.post(
            '{}{}'.format(self.server, url), 
            data=json.dumps(data), 
            headers=self._headers,
            verify = False
        )
        return resp
        pass
        
    def put(self, url, data):
        resp = self.session.put(
            '{}{}'.format(self.server, url), 
            data=data, 
            headers=self._headers,
            verify=False
        )
        return resp.ok
        pass
    def put_with_resp(self, url, data):
        resp = self.session.put(
            '{}{}'.format(self.server, url), 
            data=json.dumps(data), 
            headers=self._headers,
            verify=False
        )
        return resp
        pass

    def delete(self, url):
        resp = self.session.delete(
            '{}{}'.format(self.server, url),
            headers=self._headers
        )
        return resp
        pass