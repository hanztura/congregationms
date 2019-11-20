from mailing.models import UserMail, Mail
from pioneering.models import Pioneer
from publishers.models import (
    Asset, Publisher, Group as PublisherGroup, Member, UserGroup)
from reports.models import MonthlyFieldService
from servants.models import Servant
from system.models import User


PERMISSIONS_DATA = [
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
