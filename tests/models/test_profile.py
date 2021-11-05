from django.test import TestCase
from templates_app.models import Profile
from django.conf import settings
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='archana.ahlawat',
                                 email='archana.ahlawat@colorofchange.org',
                                 password='fakePassword')

    def test_tag_can_get_properties(self):
        user = User.objects.get(username='archana.ahlawat')
        profile = Profile.objects.get(user=user)
        
        self.assertEqual(str(profile), 'archana.ahlawat@colorofchange.org')