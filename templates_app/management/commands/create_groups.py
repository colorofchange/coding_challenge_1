"""
Create approvers and developers group
"""
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# Groups to create, on specific models, with specific permissions
GROUPS = ['approvers', 'developers']
MODELS = ['mailing', ]
PERMISSIONS = ['view','add' ] 


class Command(BaseCommand):
    help = 'Create approvers and developers group'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")