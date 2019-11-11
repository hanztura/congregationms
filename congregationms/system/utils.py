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
