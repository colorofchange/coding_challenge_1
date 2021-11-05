from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selection', views.select_template, name='select_template'),
    path('new/<str:template_name>', views.new_mailing, name='new_mailing'),
    path('select-mailing', views.mailings, name='mailings'),
    path('mailing/<int:mailing_id>', views.mailings, name='mailings-detail'),
    path('tags', views.get_tags, name='get-tags'),
    path('users', views.get_users, name='get-users'),
    path('filter-mailings', views.filter_mailings, name='filter-mailings'),
    path('filter-tags', views.filter_tags, name='filter-tags'),
    path('save-ak-mailer', views.save_ak_mailer, name='save-ak-mailer'),
    path('filter-templates', views.filter_templates, name='filter-templates'),
    path('approve', views.approve, name='approve'),
]