from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ServantModelForm
from .models import Servant
from system.utils import LoginAndPermissionRequiredMixin


class ServantListView(LoginAndPermissionRequiredMixin, ListView):
    model = Servant
    permission_required = 'servants.view_servant',

    def get_queryset(self):
        return super().get_queryset().select_related('publisher')


class ServantCreateView(LoginAndPermissionRequiredMixin, CreateView):
    model = Servant
    form_class = ServantModelForm
    permission_required = 'servants.add_servant'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mode'] = 'New'
        return context


class ServantDetailView(LoginAndPermissionRequiredMixin, DetailView):
    model = Servant
    permission_required = 'servants.view_servant',

    def get_queryset(self):
        return super().get_queryset().select_related('publisher')


class ServantDeleteView(LoginAndPermissionRequiredMixin, DeleteView):
    model = Servant
    permission_required = 'servants.delete_servant',
    success_url = reverse_lazy('servants:index')


class ServantUpdateView(LoginAndPermissionRequiredMixin, UpdateView):
    model = Servant
    form_class = ServantModelForm
    permission_required = 'servants.change_servant',

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mode'] = 'Edit'
        return context

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('publisher')

        return q
