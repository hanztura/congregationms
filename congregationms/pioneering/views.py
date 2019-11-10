from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import PioneerDetailFormSet
from .models import Pioneer


class PioneerListView(LoginRequiredMixin, ListView):
    model = Pioneer
    context_object_name = 'pioneers'


class PioneerDetailView(LoginRequiredMixin, DetailView):
    model = Pioneer
    context_object_name = 'pioneer'
    slug_field = 'code'


class PioneerCreateView(LoginRequiredMixin, CreateView):
    model = Pioneer
    fields = [
        'publisher', 'code', 'is_active'
    ]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['details'] = PioneerDetailFormSet(self.request.POST)
        else:
            data['details'] = PioneerDetailFormSet()

        return data


    def form_valid(self, form):
        context = self.get_context_data()
        details = context['details']

        with transaction.atomic():
            if details.is_valid():
                details.instance = self.object
                details.save()
                self.object = form.save()

        messages.success(
            self.request,
            'Successfully created new pioneer. Continue editing other details'
        )
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('pioneering:update', args=[str(self.object.code)])


class PioneerUpdateView(LoginRequiredMixin, UpdateView):
    model = Pioneer
    fields = ['publisher', 'code']
    context_object_name = 'pioneer'
    slug_field = 'code'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['details'] = PioneerDetailFormSet(self.request.POST, instance=self.object)
        else:
            data['details'] = PioneerDetailFormSet(instance=self.object)
        data['is_active'] = self.object.is_active
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        details = context['details']

        with transaction.atomic():
            if details.is_valid():
                details.instance = self.object
                details.save()
                self.object = form.save()

        messages.success(
            self.request,
            'Successfully updated.'
        )
        return super().form_valid(form)


class PioneerDeleteView(LoginRequiredMixin, DeleteView):
    model = Pioneer
    success_url = reverse_lazy('pioneering:index')

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()
