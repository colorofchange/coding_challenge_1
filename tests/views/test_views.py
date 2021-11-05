from django.contrib.auth.models import AnonymousUser, User, Group
from django.test import RequestFactory, TestCase
from django.conf import settings
from unittest import skip
from tests.testing_helpers import *
import os

from templates_app.models import Template
from layout.views import *

class ViewsTest(TestCase):
    def setUp(self):
        '''
        Setup for testing views
        '''
        Template.objects.create(name="test-template", template_type="default", ak_wrapper_id=54)
        Group.objects.create(name=settings.APPROVERS_GROUP_NAME)
        self.approvers_group = Group.objects.get(name=settings.APPROVERS_GROUP_NAME)

        self.factory = RequestFactory()
        self.user_malcom = User.objects.create_user(
            username='maclomx', 
            email='malcomx@colorofchange.org', 
            password='top_secret'
        )
        self.user_sam = User.objects.create_user(
            username='sam',
            email='sam@colorofchange.org',
            password='password123'
        )
        self.user_anon = AnonymousUser()

        self.approvers_group.user_set.add(self.user_malcom)

    def test_landing_page_anon_user(self):
        '''
        Test to ensure 
        * landing page loads for anonymous users with resposne code 200
        * Only login shows for anonymous user
        * No other options show for logged in user
        '''
        request = self.factory.get('/',)
        request.user = self.user_anon
        response = index(request)

        self.assertEqual(response.status_code, 200)

    def test_landing_page_user(self):
        '''
        Test to ensure:
        * User gets appropriate buttons
        * Regular user does not get approvals button
        '''
        request = self.factory.get('/',)
        request.user = self.user_sam

        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"New Mailing")
        self.assertContains(response,"Existing Mailing")
        self.assertNotContains(response,"Approvals")

    def test_landing_page_approver(self):
        '''
        Test to check that approved users get the approval button
        Expected to always return true
        '''
        request = self.factory.get('/',)
        request.user = self.user_malcom

        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"New Mailing")
        self.assertContains(response,"Existing Mailing")
        self.assertContains(response,"Approvals")
    
    def test_selection_page(self):
        '''
        Test selection page loads
        Test Anonymous users have no access
        '''

        request = self.factory.get('/selection')
        request.user = self.user_malcom
        response = select_template(request)

        self.assertEqual(response.status_code, 200)


    def test_new_mailing(self):
        '''
        Test New Mailing
        '''

        request = self.factory.get('/new')

        request.user = self.user_anon
        anon_response = new_mailing(request, "test template")

        request.user = self.user_malcom
        response = new_mailing(request, "test template")

        self.assertEqual(response.status_code, 200)

        # Send post data from form to new_mailing
        payload = {
            'csrfmiddlewaretoken': ['VVL9iGhhstst6NhVZlO2KesRxFP7dvk4mFnNlWMhisCNTF2mQXXFV7HD6Jim9grV'],
            'subjects-TOTAL_FORMS': ['3'],
            'subjects-INITIAL_FORMS': ['0'],
            'subjects-MIN_NUM_FORMS': ['0'],
            'subjects-MAX_NUM_FORMS': ['3'],
            'subjects-0-subject': ['Subject line'], 
            'subjects-0-preview_text': ['Preview Text'], 
            'subjects-0-id': [''], 
            'subjects-0-mailing': [''], 
            'subjects-1-subject': [''], 
            'subjects-1-preview_text': [''], 
            'subjects-1-id': [''], 
            'subjects-1-mailing': [''], 
            'subjects-2-subject': [''], 
            'subjects-2-preview_text': [''], 
            'subjects-2-id': [''], 
            'subjects-2-mailing': [''], 
            'from_line': ['me@me.com'], 
            'reply_to': ['me@me.com'], 
            'body': ['<p>This is the body</p>\r\n'], 
            'notes': ['These are notes'], 
            'tag_own': ['Angela'], 
            'tag_dept': ['CriminalJustice'], 
            'tag_i': ['CORPORATE ACCOUNTABILITY'], 
            'tag_oth': ['2020 Census Ads'], 
            'tag_ask': ['fundraiser'], 
            'tag_ent': ['C3'], 
            'tag_tgt': ['Appeal'], 
            'tag_camp': ['16 WNBA'], 
            'template': Template.objects.get(name="test-template").id
            }

        make_template("test-template")
        request = self.factory.post('/new', payload)
        request.user = self.user_malcom
        response = new_mailing(request, "test template")

        # Redirect occurs on successful save
        self.assertEqual(response.status_code, 302)
        delete_template("test-template")



    def test_mailings(self):
        '''
        Test list mailings
        '''

        request = self.factory.get('/mailings')

        request.user = self.user_anon
        anon_response = mailings(request)

        request.user = self.user_malcom
        response = mailings(request)

        self.assertEqual(response.status_code, 200)

    def test_get_tags(self):
        '''
        Test get tags
        '''

        request = self.factory.get('/tags')

        request.user = self.user_anon
        anon_response = get_tags(request)

        request.user = self.user_malcom
        response = get_tags(request)

        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        '''
        Test get users
        '''

        request = self.factory.get('/users')

        request.user = self.user_anon
        anon_response = get_users(request)

        request.user = self.user_malcom
        response = get_users(request)

        self.assertEqual(response.status_code, 200)
