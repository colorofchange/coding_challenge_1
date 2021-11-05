from stout.settings import TAG_SOURCE_NAMES
from django import forms
from django.conf import settings
from .models import Mailing, Tag, MailingSubject
from helpers.litmus import Litmus
import datetime
from django.forms import inlineformset_factory, BaseInlineFormSet, HiddenInput


class BaseMailingFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseMailingFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['subject'].widget.attrs.update(
                {'placeholder': settings.MAILER_FORM_PLACEHOLDERS['subject']})
            form.fields['preview_text'].widget.attrs.update(
                {'placeholder': settings.MAILER_FORM_PLACEHOLDERS['preview_text']})


MailingFormSet = inlineformset_factory(Mailing, MailingSubject, formset=BaseMailingFormSet, fields=(
    'subject', 'preview_text'), extra=0)


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ['ak_mailer_id', 'tags', 'email_guid',
                   'email_creator', 'email_wrapper']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'template' and field != 'approved':
                self.fields[field].widget.attrs.update(
                    {'placeholder': settings.MAILER_FORM_PLACEHOLDERS[field]})
            if field == 'body':
                self.fields[field].widget.config['editorplaceholder'] = settings.MAILER_FORM_PLACEHOLDERS[field]

        if not self.can_user_approve(self.user):
            self.fields["approved"].widget = HiddenInput()

    def save(self, commit=True):
        mailing = super(MailingForm, self).save()
        mailing.tags.set([])
        mailing.save()

        for tag in settings.TAGS:
            _tag = tag[0].lower()
            if (self.cleaned_data[f"tag_{_tag}"]):
                tag_search = [_t.strip()
                              for _t in self.cleaned_data[f"tag_{_tag}"].split(',')]
                if ((_tag == 'oth' or _tag == 'camp' or _tag == 'own' or _tag == 'help') and len(tag_search) > 0): # tags that campaigners can create
                    new_tags = []
                    for tag in tag_search:
                        try:
                            new_tag_to_add = Tag.objects.get(name=tag, tag_type=_tag)
                        except Tag.DoesNotExist:
                            new_tag_to_add = None

                        if new_tag_to_add == None:
                            if _tag == 'oth':
                                new_tag_to_add = Tag.objects.create(
                                    name=tag, tag_type=_tag, source_name=tag)
                            else: 
                                source_prepend = settings.TAG_SOURCE_NAMES[_tag.upper()]
                                stout_name = ''
                                source = ''
                                if source_prepend.strip() in tag:
                                    source = tag 
                                    stout_name = tag.split(source_prepend)[1]
                                else: 
                                    source = source_prepend + tag
                                    stout_name = tag
                                new_tag_to_add = Tag.objects.create(
                                    name=stout_name, tag_type=_tag, source_name=source)
                            new_tag_to_add.save()
                            new_tags.append(new_tag_to_add)
                        else:
                            new_tags.append(Tag.objects.get(name=tag))
                else:
                    new_tags = Tag.objects.filter(name__in=tag_search)
                mailing.tags.add(*new_tags)
                mailing.save()

        litmus = Litmus()

        screenshot_guid = litmus.get_screenshots(
            self.cleaned_data['template'].load_template(self.cleaned_data['body']))
        mailing.email_guid = screenshot_guid
        mailing.email_creator = self.user
        return super().save()

    def can_user_approve(self, user):
        return user.groups.filter(name=settings.APPROVERS_GROUP_NAME).exists()
