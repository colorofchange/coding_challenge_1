from helpers.ak_wrapper import ActionKit
from django.test import TestCase
from django.conf import settings

class ActionKitTestCase(TestCase):
    conn = None
    def setUp(self):
       self.conn = ActionKit()

    def tests_ak_connection(self):
        get_response = self.conn.get('')
        post_response = self.conn.post('')
        patch_response = self.conn.patch('', None)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 200)

    def tests_ak_tags_endpoint(self):
        get_response = self.conn.get(settings.TAG_ENDPOINT)
        self.assertEqual(get_response.status_code, 200)

        #post_response = self.conn.post(settings.TAG_ENDPOINT, {'name': 'superspecifictag'})
        #self.assertEqual(post_response.status_code, 201)
        # This works, but we don't want to test this out all the time and create so many new tags

    def tests_ak_mailer_endpoint(self):
        get_response = self.conn.get(settings.MAILER_ENDPOINT)
        self.assertEqual(get_response.status_code, 200)
        
    # Other tests for: updating mailers, creating mailers