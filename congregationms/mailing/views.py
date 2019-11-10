from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import reverse

from .forms import MailModelForm
from .models import Mail


class MailCreateView(LoginRequiredMixin, CreateView):
    form_class = MailModelForm
    model = Mail

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['attachment'] = self.request.GET.get('filename')
        return initial

    def get_success_url(self, *args, **kwargs):
        return reverse('publishers:index')


    def form_valid(self, form):
        _value = super().form_valid(form)

        if form.send_email():
            messages.success(
                self.request,
                'Successfully shared via email!')
        else:
            messages.error(
                self.request,
                'Something went wrong. Unable to share via email. Please check your internet connection.')
        return _value
