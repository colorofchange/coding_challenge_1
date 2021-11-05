from django.test import TestCase
from templates_app.models import Template
from tests.testing_helpers import *

class TemplateTestCase(TestCase):
    def setUp(self):
        Template.objects.create(name='Best Template', template_type='test_template')

    def test_template_can_get_properties(self):
        template = Template.objects.get(name='best template')
        
        self.assertEqual(template.get_template_name(), 'best template')
        self.assertEqual(template.get_template_type(), 'test_template')

    def test_template_can_load_html(self):
        template = Template.objects.get(name='best template')
        make_template(template.name)

        template_html = template.load_template('This is my body content. Special word: Mister Mxyzptlk')
        self.assertIs(type(template_html), str)
        self.assertIn('<html>', template_html )
        self.assertIn('Mxyzptlk', template_html )
        self.assertIn('</html>', template_html )

        delete_template(template.name)
        self.assertEqual(template.get_template_file_name(), 'best-template.html')

