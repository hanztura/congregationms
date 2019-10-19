from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully created new pioneer. Continue editing other details'
        )
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('pioneering:update', args=[str(self.publisher.slug)])


class PioneerUpdateView(LoginRequiredMixin, UpdateView):
    model = Pioneer
    fields = [
        'publisher', 'code', 'is_active'
    ]
    context_object_name = 'pioneer'
    slug_field = 'code'


class PioneerDeleteView(LoginRequiredMixin, DeleteView):
    model = Pioneer

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()
