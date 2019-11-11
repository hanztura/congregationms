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
        authorized_groups = self.request.authorized_groups
        if authorized_groups:
            _members = [g.group.group_members.filter(is_active=True) for g in authorized_groups]
            members = []
            for mem in _members:
                for m in mem:
                    members.append(m.publisher_id)
            # members = [m.publisher_id for m in members]
            queryset = Publisher.objects.filter(id__in=members)
        else:
            queryset = self.model.objects.none()

        return queryset


class PublisherUpdate(LoginAndPermissionRequiredMixin, UpdateView):
    model = Publisher
    fields = ['last_name', 'first_name', 'middle_name',
              'date_of_birth', 'date_of_baptism', 'contact_numbers', 'slug']
    context_object_name = 'publisher'
    permission_required = 'publishers.change_publisher',


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
        queryset = super().get_queryset()

        user = self.request.user
        group = user.publisher.group
        if group:
            queryset = queryset.filter(id=group.pk)

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
