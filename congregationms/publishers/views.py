#from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import GroupMemberForm, GroupMemberFormSet, PublisherModelForm
from .models import Group, Publisher


# Create your views here.
class PublisherList(LoginRequiredMixin, ListView):
    model = Publisher


class PublisherUpdate(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ['last_name', 'first_name', 'middle_name',
              'date_of_birth', 'date_of_baptism', 'contact_numbers', 'slug']
    context_object_name = 'publisher'


class PublisherDetail(LoginRequiredMixin, DetailView):
    model = Publisher
    context_object_name = 'publisher'


class PublisherCreate(LoginRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherModelForm

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully created new publisher. Continue editing other details'
        )
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('publishers:update', args=[str(self.object.slug)])


class PublisherDelete(LoginRequiredMixin, DeleteView):
    model = Publisher
    success_url = reverse_lazy('publishers:index')

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()


class GroupList(LoginRequiredMixin, ListView):
    model = Group


class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    context_object_name = 'group'


class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    fields = [
        'name', 'congregation'
    ]
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = GroupMemberFormSet(self.request.POST, instance=self.object)
        else:
            data['members'] = GroupMemberFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']

        print(members.errors)
        with transaction.atomic():
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()

        messages.success(
            self.request,
            'Successfully edited Group {}.'.format(str(self.object))
        )
        return super().form_valid(form)


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('publishers:group-index')

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()


class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'congregation']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = GroupMemberFormSet(self.request.POST)
        else:
            data['members'] = GroupMemberFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']

        with transaction.atomic():
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()

        messages.success(
            self.request,
            'Successfully created new Group {}.'.format(str(self.object))
        )
        return super().form_valid(form)
