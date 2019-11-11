from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)


class LoginAndPermissionRequiredMixin(
        LoginRequiredMixin, PermissionRequiredMixin):
    pass
