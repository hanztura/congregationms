from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Congregation, Setting

# Register your models here
admin.site.register(User, UserAdmin)
# admin.site.register(Congregation)
admin.site.register(Setting)
