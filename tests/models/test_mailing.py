from django.test import TestCase
from templates_app.models import Mailing, Tag, Template, MailingSubject
from django.contrib.auth.models import User

class MailingTestCase(TestCase):
    def setUp(self):
        tag = Tag.objects.create(name='Test Tag')
        tag2 = Tag.objects.create(name="Test Tag 2")
        user = User.objects.create_user(username='archana.ahlawat',
                                 email='archana.ahlawat@colorofchange.org',
                                 password='fakePassword')
        template = Template.objects.create(name='Best Template', template_type='test_template')
        mailing = Mailing.objects.create(
            from_line='products@colorofchange.org',
            reply_to = 'products@colorofchange.org',
            body = 'body text.',
            template = template,
            approved = False,
            email_creator= user
        )
        mailing.tags.set([tag, tag2])

    def test_mailing_setup(self):
        mailing = Mailing.objects.get(from_line='products@colorofchange.org')

        self.assertEqual(mailing.body, 'body text.')
        self.assertEqual(mailing.notes, None)
        self.assertEqual(mailing.email_creator, User.objects.get(username='archana.ahlawat'))
        self.assertEqual(mailing.template, Template.objects.get(name='best template'))
        self.assertTrue(mailing.tags.filter(name='Test Tag').exists())
        self.assertTrue(mailing.tags.filter(name='Test Tag 2').exists())

    def test_mailing_approval_process(self):
        mailing = Mailing.objects.get(from_line='products@colorofchange.org')

        self.assertEqual(mailing.approved, False)
        mailing.approve()
        self.assertEqual(mailing.approved, True)

    def test_mailing_add_notes(self):
        mailing = Mailing.objects.get(from_line='products@colorofchange.org')

        mailing.notes = 'mailer notes'
        mailing.save()
        self.assertEqual(mailing.notes, 'mailer notes')

    def test_mailing_subject_relationship(self):
        mailing = Mailing.objects.get(from_line='products@colorofchange.org')

        self.assertEqual(str(mailing), 'No Subject')
        
        MailingSubject.objects.create(mailing=mailing, subject="Important Email", preview_text="Important Email's preview text")

        self.assertEqual(str(mailing), "Important Email")

        MailingSubject.objects.create(mailing=mailing, subject="Important Email 2", preview_text="Important Email's preview text")
        self.assertEqual(str(mailing), "Important Email")
        self.assertTrue(mailing.subjects.filter(subject="Important Email 2").exists())