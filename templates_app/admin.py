from django.contrib import admin
from .models import Template, Tag, Mailing, Profile, MailingSubject

admin.site.register(Template)
admin.site.register(Tag)
admin.site.register(Mailing)
admin.site.register(Profile)
admin.site.register(MailingSubject)