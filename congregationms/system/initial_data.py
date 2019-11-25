from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import User
from mailing.models import UserMail, Mail
from pioneering.models import Pioneer
from publishers.models import (
    Asset, Publisher, Group as PublisherGroup, Member, UserGroup)
from reports.models import MonthlyFieldService
from servants.models import Servant

def make_initial_data_for_auth_group_permission():
    permissions = Permission.objects.all()
    groups = Group.objects.all()
    data = [
        {
            'id': 1,
            'name': 'Master Users',
            'permissions': [
                {
                    'model': UserMail,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Mail,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Pioneer,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Asset,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Publisher,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': PublisherGroup,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Member,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': UserGroup,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': MonthlyFieldService,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Servant,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': User,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
            ]
        },  # master users
        {
            'id': 2,
            'name': 'Group Leaders',
            'permissions': [
                {
                    'model': UserMail,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Mail,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Pioneer,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Publisher,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Member,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': MonthlyFieldService,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Servant,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
            ]
        },  # group leaders
        {
            'id': 3,
            'name': 'Group Assistants',
            'permissions': [
                {
                    'model': Pioneer,
                    'allows': [
                        'view',
                    ]
                },
                {
                    'model': Publisher,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': Member,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
                {
                    'model': MonthlyFieldService,
                    'allows': [
                        'add',
                        'change',
                        'delete',
                        'view',
                    ]
                },
            ]
        },  # group assistants
        {
            'id': 4,
            'name': 'Publishers',
            'permissions': [
                {
                    'model': Publisher,
                    'allows': [
                        'change',
                        'view',
                    ]
                },
                {
                    'model': MonthlyFieldService,
                    'allows': [
                        'add',
                    ]
                },
            ]
        },
    ]
    for d in data:
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

make_initial_data_for_auth_group_permission()
