#from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import GroupMemberForm, GroupMemberFormSet, PublisherModelForm
from .models import Group, Publisher
from system.utils import LoginAndPermissionRequiredMixin


# Create your views here.
class PublisherList(LoginAndPermissionRequiredMixin, ListView):
    model = Publisher
    permission_required = 'publishers.view_publisher',

    def get_queryset(self):
        auth_pubs = self.request.authorized_publisher_pks
        if auth_pubs:
            queryset = Publisher.objects.filter(id__in=auth_pubs)
        else:
            queryset = self.model.objects.none()

        return queryset


class PublisherUpdate(LoginAndPermissionRequiredMixin, UpdateView):
    model = Publisher
    form_class = PublisherModelForm
    context_object_name = 'publisher'
    permission_required = 'publishers.change_publisher',

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully updated.'
        )
        return super().form_valid(form)


class PublisherDetail(LoginAndPermissionRequiredMixin, DetailView):
    model = Publisher
    context_object_name = 'publisher'
    permission_required = 'publishers.view_publisher',


class PublisherCreate(LoginAndPermissionRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherModelForm
    permission_required = 'publishers.add_publisher',

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully created new publisher. Continue editing other details'
        )
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('publishers:update', args=[str(self.object.slug)])


class PublisherDelete(LoginAndPermissionRequiredMixin, DeleteView):
    model = Publisher
    success_url = reverse_lazy('publishers:index')
    permission_required = 'publishers.delete_publisher',

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()


class GroupList(LoginAndPermissionRequiredMixin, ListView):
    model = Group
    permission_required = 'publishers.view_group',

    def get_queryset(self):
        queryset = self.model.objects.none()

        # user = self.request.user
        # publisher = user.publisher
        # group = publisher.group_members.filter(is_active=True)
        # group = group.first()  # publishers.Member object
        # if group:
        #     queryset = super().get_queryset()
        #     queryset = queryset.filter(id=group.group_id)
        groups = self.request.authorized_groups  # publisher.UserGroup objects
        if groups:
            groups = [g.group_id for g in groups]  # Group pks
            queryset = super().get_queryset().filter(id__in=groups)
            queryset = queryset.select_related('congregation')

        return queryset


class GroupDetail(LoginAndPermissionRequiredMixin, DetailView):
    model = Group
    context_object_name = 'group'
    permission_required = 'publishers.view_group',


class GroupUpdate(LoginAndPermissionRequiredMixin, UpdateView):
    model = Group
    fields = [
        'name', 'congregation'
    ]
    context_object_name = 'group'
    permission_required = 'publishers.change_group',

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


class GroupDelete(LoginAndPermissionRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('publishers:group-index')
    permission_required = 'publishers.delete_group',

    def get_success_url(self):
        messages.success(
            self.request,
            'Successfully deleted {}.'.format(str(self.object))
        )
        return super().get_success_url()


class GroupCreate(LoginAndPermissionRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'congregation']
    permission_required = 'publishers.add_group',

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
