from django.test import TestCase
from templates_app.models import Tag
from django.conf import settings

class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Test Tag', source_name='Test Tag')

    def test_tag_can_get_properties(self):
        tag = Tag.objects.get(name='Test Tag')
        
        self.assertEqual(str(tag), 'Test Tag')
        self.assertEqual(tag.tag_type, 'OTH') # default tag type

        tag.tag_type = settings.TAGS[2][0]
        self.assertEqual(tag.tag_type, 'HELP')
