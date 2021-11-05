import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import json

class Litmus():
    username = settings.LITMUS_KEY
    password = '' # Password is always blank
    root_url = 'https://instant-api.litmus.com/v1/'
    headers = {'Content-Type': 'application/json'}
    
    def get(self, endpoint, params={}):
        response = requests.get(
            f'{self.root_url}{endpoint}',
            params,
            auth=HTTPBasicAuth(self.username, self.password),
            headers=self.headers
            )
        return response 

    def post(self, endpoint, data={}):
        response = requests.post(
            f'{self.root_url}{endpoint}',
            json=data,
            auth=HTTPBasicAuth(self.username, self.password)
            )
        return response

    def get_screenshots(self, data):
       response = self.post('emails',{"html_text":data})
       json_data = json.loads(response.content.decode("utf-8"))
       return json_data['email_guid']
