from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup


class Template(models.Model):
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=100)
    ak_wrapper_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_template_name(self):
        return self.name

    def get_template_type(self):
        return self.template_type

    def get_template_file_name(self):
        return self.name.replace(" ", "-") + ".html"

    def load_template(self, body):
        parsed_template = None
        file = None
        template_location = settings.TEMPLATES_LOCATION + \
            self.get_template_file_name()

        with open(template_location) as file:
            try:
                parsed_template = BeautifulSoup(file, 'html.parser')
                parsed_template.find_all(
                    class_="body-text")[0].string = body
            except:
                pass
            finally:
                file.close()

        return str(parsed_template.prettify(formatter=None))

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.template_type = self.template_type.lower()
        return super(Template, self).save(*args, **kwargs)


class Tag(models.Model):
    # Class for holding AK tags
    name = models.CharField(max_length=100)
    tag_type = models.CharField(
        max_length=255, choices=settings.TAGS, default=settings.TAGS[0][0])
    source_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tag_type = self.tag_type.upper()
        return super(Tag, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ak_auth_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Mailing(models.Model):
    email_creator = models.ForeignKey(
        User, related_name='emails', on_delete=models.CASCADE, blank=True, null=True)
    from_line = models.CharField(max_length=255, blank=True)
    reply_to = models.CharField(max_length=255, blank=True)
    body = RichTextUploadingField(blank=True)
    notes = models.TextField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(
        Tag, related_name='email_editions', blank=True)
    tag_own = models.CharField(max_length=100, blank=True, null=True)
    tag_help = models.CharField(max_length=100, blank=True, null=True)
    tag_dept = models.CharField(max_length=100, blank=True, null=True)
    tag_i = models.CharField(max_length=100, blank=True, null=True)
    tag_oth = models.CharField(max_length=100, blank=True, null=True)
    tag_ask = models.CharField(max_length=100, blank=True, null=True)
    tag_ent = models.CharField(max_length=100, blank=True, null=True)
    tag_tgt = models.CharField(max_length=100, blank=True, null=True)
    tag_camp = models.CharField(max_length=100, blank=True, null=True)
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField()
    ak_mailer_id = models.IntegerField(null=True, blank=True)
    email_guid = models.CharField(max_length=64, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    email_wrapper = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-updated_date']

    # Need to install django_auth
    # approved_by = models.ManyToManyField(Auth_Users,related_name='users')

    def __str__(self):
        if self.subjects.first():
            return self.subjects.first().subject
        else:
            return "No Subject"

    def approve(self):
        self.approved = True
        self.save()
        return None


class MailingSubject(models.Model):
    mailing = models.ForeignKey(
        Mailing, related_name='subjects', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    preview_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.subject
