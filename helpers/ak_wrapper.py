import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from bs4 import BeautifulSoup 
from helpers.util import esc_ent

class ActionKit():
    username = settings.AK_USERNAME
    password = settings.AK_PASSWORD
    root_url = 'https://act.colorofchange.org/rest/v1/'
    
    def get(self, endpoint, params={}):
        response = requests.get(
            '{}{}'.format(self.root_url,endpoint),
            params,
             auth=HTTPBasicAuth(self.username, self.password)
            )
        return response 

    def post(self, endpoint, data={}):
        response = requests.post('{}{}'.format(self.root_url,endpoint), json=data,
            auth=HTTPBasicAuth(self.username, self.password)
            )
        return response

    def patch(self, endpoint, resource_location='', data={}):
        response = requests.patch('{}{}/{}'.format(self.root_url,endpoint,resource_location), json=data,
            auth=HTTPBasicAuth(self.username, self.password)
            )
        return response
      
    def save_in_ak(self, mailing):
        conn = self

        if (mailing.email_creator.profile.ak_auth_id == None):
            response = conn.get(settings.AUTHUSERS_ENDPOINT, {'email': mailing.email_creator.email})
            mailing.email_creator.profile.ak_auth_id = int(response.json()['objects'][0]['id'])
            mailing.email_creator.profile.save()
        authuser_uri = "/rest/v1/authuser/" + str(mailing.email_creator.profile.ak_auth_id) + '/'
        emailwrapper_uri = "/rest/v1/emailwrapper/" + str(mailing.template.ak_wrapper_id) + '/'
    
        subject_list = []
        preview_text_list = []
        tag_list = []
        for subject in mailing.subjects.all():
            subject_list.append(esc_ent(subject.subject))
            preview_text_list.append(esc_ent(subject.preview_text))
        for tag in mailing.tags.all():
            tag_list.append(esc_ent(tag.source_name))

        body = {
            'subjects': subject_list,
            'preview_text': preview_text_list,
            'fromline': esc_ent(mailing.from_line),
            'html': esc_ent(mailing.body),
            'reply_to': esc_ent(mailing.reply_to),
            'submitter': authuser_uri,
            'scheduled_by': authuser_uri,
            'tags': tag_list,
            'emailwrapper': emailwrapper_uri,
            'notes': esc_ent(mailing.notes)
        }
        if mailing.ak_mailer_id is not None: # this mailer exists in AK
            response = conn.patch(settings.MAILER_ENDPOINT, str(mailing.ak_mailer_id), body)

        else: 
            response = conn.post(settings.MAILER_ENDPOINT, body)
            if response.status_code == 201:
                mailing.ak_mailer_id = int(response.headers['location'].split('/')[-2])
        mailing.save()
