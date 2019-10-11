from django.contrib import admin

from .models import Publisher, Group, Member


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Group)
admin.site.register(Member)
