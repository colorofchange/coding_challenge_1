from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from templates_app.models import Template, Mailing, Tag
from django.contrib.auth.models import User
from templates_app.forms import MailingForm, MailingFormSet
from helpers.litmus import Litmus
from django.conf import settings
from django.core.paginator import Paginator
from django.core import serializers
from helpers.ak_wrapper import ActionKit


def index(request):
    return render(
        request,
        'layout/pages/index.html',
        {
            'user_can_approve': request.user.groups.filter(name=settings.APPROVERS_GROUP_NAME).exists()
        }
    )


def select_template(request):
    templates = {}
    template_types = Template.objects.order_by(
        "template_type").values_list('template_type').distinct()
    for template_type in template_types:
        templates[template_type[0]] = Template.objects.filter(
            template_type=template_type[0])

    return render(request, 'layout/pages/select-template.html', {'template_types': template_types, 'templates': templates})


def new_mailing(request, template_name):
    context = {
        'display_details': False,
        'mailing_clients': settings.MAILING_CLIENTS,
    }
    template = Template.objects.get(name=template_name.replace(" ", "-"))

    context['template'] = template.name.replace(" ", "-")

    context['form'] = MailingForm(
        initial={'template': template.id}, user=request.user)
    formset = MailingFormSet()
    context['formset'] = formset
    if request.method == 'POST':
        form = MailingForm(request.POST, user=request.user)
        context['form'] = form
        if form.is_valid():
            instance = form.save()
            instance.save()
            context['display_details'] = True
        formset = MailingFormSet(request.POST, instance=instance)
        if formset.is_valid():
            formset.save()
        formset = MailingFormSet(instance=instance)
        context['formset'] = formset

        return redirect('/mailing/' + str(instance.pk))

    return render(request, 'layout/pages/mailing.html', context)


def mailings(request, mailing_id=None):
    context = {
        'display_details': True,
        'mailing_clients': settings.MAILING_CLIENTS,
        'instructions': 'List of all mailings',
    }
    if mailing_id == None:
        # TODO: Get all mailings and and a Paginator. 
        # Paginator should be 10 items per page
        # render expects a request, path to an HTML file and a context dictonary
        # You can pass extra content into the context variable, which can then be used in the template (selct-mailing.html)
        paginator = Paginator(Mailing.objects.all(), 10)
        page = request.GET.get('page')
        context['mailings'] = paginator.get_page(page)
        print(context['mailings'])
        # No changes should be required past here.
        return render(request, 'layout/pages/select-mailing.html', context)

    instance = Mailing.objects.get(pk=mailing_id)

    context['approval_status'] = instance.approved
    context['ak_id'] = '' if instance.ak_mailer_id is None else instance.ak_mailer_id

    tags = instance.tags.values()
    template_types = list(instance.tags.values_list('tag_type').distinct())
    initial = {}

    for template_type in template_types:
        _tempalte_type_name = template_type[0].lower()
        flat_list_tags = map(
            lambda val: val[0],
            list(tags.filter(tag_type__iexact=_tempalte_type_name).values_list('name')
                 ))

        initial[f"tag_{_tempalte_type_name}"] = ', '.join(list(flat_list_tags))

    context['template'] = instance.template.name.replace(" ", "-")
    mailing_subjects = MailingFormSet(instance=instance)
    mailing = MailingForm(
        instance=instance, initial=initial, user=request.user)
    context['formset'] = mailing_subjects
    context['form'] = mailing
    if request.method == 'POST':
        mailing = MailingForm(
            request.POST, instance=instance, user=request.user)
        if mailing.is_valid():
            mailing.save()
        context['form'] = mailing
        formset = MailingFormSet(request.POST, instance=instance)
        if formset.is_valid():
            formset.save()
        formset = MailingFormSet(instance=instance)
        context['formset'] = formset
        context['msg'] = 'Form Saved'

    return render(request, 'layout/pages/mailing.html', context)


def get_tags(request):
    payload = []
    if request.GET.get('full') == None:
        t_type = request.GET.get('tag_type')
        tags = list(Tag.objects.filter(
            tag_type=t_type).values_list('name').distinct())
        for tag in tags:
            payload.append(tag[0])
        payload.sort()
        return JsonResponse(payload, safe=False)
    else:
        payload = []
        full_tag_list = list(Tag.objects.all().values_list('name').distinct())
        for tag in full_tag_list:
            payload.append(tag[0])

        payload.sort()
        return JsonResponse(payload, safe=False)


def get_users(request):
    payload = []
    users = User.objects.all().values_list('username')
    return JsonResponse(users[0], safe=False)


def filter_mailings(request):
    filter_type = request.POST.get('type').lower()
    value = request.POST.get('value')

    if filter_type == "tag":
        tag_search_terms = value.split(",")
        tag = Tag.objects.get(name=tag_search_terms[0])
        mailings = Mailing.objects.filter(tags=tag)
    elif filter_type == "user":
        user_search_terms = value.split(",")
        user = User.objects.get(username=user_search_terms[0])
        mailings = Mailing.objects.filter(email_creator=user)

    return JsonResponse(list(mailings.values('updated_date', 'subjects__subject', 'id')), safe=False)


def filter_tags(request):
    value = request.POST.get('value').split(",")[0]
    tag_type = request.POST.get('tag_type')

    #tags = Tag.objects.filter(tag_type=tag_type).filter(name__icontains=value)
    tags = Tag.objects.filter(name__icontains=value)
    return JsonResponse(list(tags.values()), safe=False)


def save_ak_mailer(request):
    mailing_id = request.POST.get('mailing_id')
    mailing = Mailing.objects.get(pk=mailing_id)
    conn = ActionKit()
    conn.save_in_ak(mailing)
    return JsonResponse(mailing.ak_mailer_id, safe=False)


def filter_templates(request):
    template_type = request.POST.get('template_type')
    templates = Template.objects.filter(template_type=template_type).values()
    return JsonResponse(list(templates), safe=False)


def approve(request):
    mailings = Mailing.objects.filter(approved=False)

    paginator = Paginator(mailings, 10)
    page_number = request.GET.get('page')
    page_mailings = paginator.get_page(page_number)

    context = {
        'mailings': mailings,
        'page_mailings': page_mailings,
        'instructions': 'Mailings waiting to be approved',
    }
    return render(request, 'layout/pages/select-mailing.html', context)
