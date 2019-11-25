from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from ._constants import PERMISSIONS_DATA
from system.models import Setting


class Command(BaseCommand):
    """Set up system initial data.

    Auth Group Permissions
    """
    help = 'Set up system initial data'

    @transaction.atomic
    def handle(self, *args, **options):
        setting, created = Setting.objects.get_or_create(pk=1)

        msg = 'Attempting to create initial data...'
        print(msg)
        if not setting.initial_data_runned:
            permissions = Permission.objects.all()
            groups = Group.objects.all()

            for d in PERMISSIONS_DATA:
                group = groups.get(id=d['id'])

                # get permission
                data_perms = d['permissions']
                permissions_allowed = []
                for data_perm in data_perms:
                    model = data_perm['model']
                    model_name = model.__name__.lower()
                    allows = data_perm['allows']
                    content_type = ContentType.objects.get_for_model(model)
                    p1 = permissions.filter(content_type=content_type.pk)

                    for allow in allows:  # view, add, change, delete
                        codename = '{}_{}'.format(allow, model_name)
                        p2 = p1.get(codename=codename)
                        permissions_allowed.append(p2)

                group.permissions.add(*permissions_allowed)

            setting.initial_data_runned = True
            setting.save()
            msg = 'Successfully created initial data!!!'
            print(msg)
            return
