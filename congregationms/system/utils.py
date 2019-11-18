import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)


class LoginAndPermissionRequiredMixin(
        LoginRequiredMixin, PermissionRequiredMixin):
    pass


class AddUserToFormMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AddRequestToForm:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


def compute_age(birthdate, on_date=None):
    if on_date is None:
        on_date = datetime.date.today()

    age = on_date - birthdate  # timedelta
    age = age.days // 365
    return age
