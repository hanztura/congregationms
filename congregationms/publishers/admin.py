from django.contrib import admin

from .models import Asset, Publisher, Group, Member, UserGroup


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(UserGroup)
admin.site.register(Asset)
