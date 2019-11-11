

from datetime import datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MFSForm
from .models import MonthlyFieldService
from .utils import (compute_month_year, generate_mfs, aggregate_mfs_queryset,
                    get_mfs_data, get_months_and_years)
from publishers.models import Publisher, Group
from publishers.utils import get_user_groups_members
from system.utils import LoginAndPermissionRequiredMixin, AddRequestToForm


class MFSList(LoginAndPermissionRequiredMixin, ListView):
    """MFS stands for Month Field Service."""
    model = MonthlyFieldService
    permission_required = 'reports.view_monthlyfieldservice',

    def get_queryset(self):
        now = datetime.now().date()
        default_month_year = compute_month_year(now)
        monthyear = self.request.GET.get('monthyear', default_month_year)
        monthyear = monthyear.split('-')
        year = monthyear[0]
        month = monthyear[1]
        queryset = MonthlyFieldService.objects.filter(
            month_ending__year=year,
            month_ending__month=month
        ).select_related('pioneering', 'publisher', 'group')

        # filter mfs of user's group only
        auth_pubs = self.request.authorized_publisher_pks
        if auth_pubs:
            queryset = queryset.filter(publisher__in=auth_pubs)
        else:
            queryset = self.model.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        now = datetime.now().date()
        default_month_year = compute_month_year(now)
        monthyear = self.request.GET.get('monthyear', default_month_year)
        context = super().get_context_data(**kwargs)
        context['monthyear'] = monthyear
        return context


class MFSDelete(LoginAndPermissionRequiredMixin, DeleteView):
    model = MonthlyFieldService
    success_url = reverse_lazy('reports:mfs-index')
    permission_required = 'reports.delete_monthlyfieldservice',

    def get_success_url(self):
        message = "Successfully deleted."
        messages.success(self.request, message)
        return super().get_success_url()


class MFSDetail(LoginAndPermissionRequiredMixin, DetailView):
    model = MonthlyFieldService
    context_object_name = 'report'
    permission_required = 'reports.view_monthlyfieldservice',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_rp'] = False
        if self.object.pioneering:
            if self.object.pioneering.pioneer_type == 'RP':
                context['is_rp'] = True

        pioneering = self.object.pioneering
        if pioneering:
            context['pioneering'] = pioneering.pioneer_type

        context['publisher_slug'] = self.object.publisher.slug

        return context


class MFSCreate(
        AddRequestToForm, LoginAndPermissionRequiredMixin, CreateView):
    model = MonthlyFieldService
    form_class = MFSForm
    permission_required = 'reports.add_monthlyfieldservice',

    def form_valid(self, form):
        try:
            form = super().form_valid(form)
            msg = 'Successfully created new \
                    Monthly Field Service Report of {}.'
            msg = msg.format(str(self.object))
            messages.success(
                self.request,
                msg
            )
        except Exception as e:
            raise e
        finally:
            return form

    def get_success_url(self):
        another = self.request.GET.get('another', False)
        if another:
            return reverse_lazy('reports:mfs-create')

        return super().get_success_url()


class MFSUpdate(
        AddRequestToForm, LoginAndPermissionRequiredMixin, UpdateView):
    model = MonthlyFieldService
    form_class = MFSForm
    context_object_name = 'report'
    permission_required = 'reports.change_monthlyfieldservice',


class MFSHistoryList(LoginAndPermissionRequiredMixin, ListView):
    model = MonthlyFieldService
    template_name = 'reports/mfs_history.html'
    context_object_name = 'reports'
    permission_required = 'reports.view_monthlyfieldservice',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['totals'] = aggregate_mfs_queryset(context['reports'])

        view_type = self.kwargs['view_type']  # publisher or group

        if view_type == 'publisher':
            publisher = self.kwargs['publisher']
            publisher = Publisher.objects.get(slug=publisher)
            context['publisher'] = publisher
        else:
            group = self.kwargs['group']
            group = Group.objects.get(pk=group)
            context['group'] = group

        # date from and date to for default date search value
        now = datetime.now().date()
        date_from = self.request.GET.get('from', str(now))
        date_to = self.request.GET.get('to', str(now))

        dates = get_months_and_years(date_from, date_to)

        context['from'] = dates['df']
        context['to'] = dates['dt']
        return context

    def get_queryset(self):
        view_type = self.kwargs['view_type']  # publisher or group

        now = datetime.now().date()
        date_from = self.request.GET.get('from', str(now))
        date_to = self.request.GET.get('to', str(now))

        is_vt_publisher = view_type == 'publisher'  # view type publisher
        if is_vt_publisher:
            publisher = self.kwargs['publisher']
            publisher = Publisher.objects.get(slug=publisher)

            data = get_mfs_data(
                date_from, date_to, publisher.pk, is_vt_publisher)
        else:
            group_pk = self.kwargs['group']

            data = get_mfs_data(date_from, date_to, group_pk, is_vt_publisher)

        return data['queryset']


@login_required
@permission_required('reports.view_monthlyfieldservice', raise_exception=True)
def sample_mfs(request, pk):
    now = datetime.now().date()
    date_from = request.GET.get('from', str(now))
    date_to = request.GET.get('to', str(now))

    data = get_mfs_data(date_from, date_to, pk, False)

    group = data['group']
    period = '{} to {}'.format(data['from'], data['to'])

    data = {
        'queryset': data['queryset'],
        'group': group.name,
        'congregation': str(group.congregation),
        'month': period,
        'totals': data['totals'],
    }
    fullpath = generate_mfs(data)['fullpath']
    return FileResponse(
        open(fullpath, 'rb'),
        as_attachment=True,
        filename='download.docx')


class ShareToRedirectView(LoginAndPermissionRequiredMixin, RedirectView):
    """Redirect to Draft Email Page.

    Generate Publisher's MFS History Document first.
    """
    permission_required = 'mailing.add_mail',

    def get_redirect_url(self, *args, **kwargs):
        publisher = get_object_or_404(Publisher, pk=self.kwargs['publisher'])
        now = datetime.now().date()
        date_from = self.request.GET.get('from', str(now))
        date_to = self.request.GET.get('to', str(now))

        data = get_mfs_data(date_from, date_to, publisher.pk)

        # if queryset is blank, redirect to referer
        referer = self.request.headers['Referer']
        if data['queryset'].count() < 1:
            messages.warning(
                self.request,
                "Unable to share MFS History with no data.")
            return referer

        congregation = str(publisher.group.congregation)
        group = publisher.group.name
        period = '{} to {}'.format(data['from'], data['to'])

        # data for mfs document
        data = {
            'queryset': data['queryset'],
            'group': group,
            'congregation': congregation,
            'month': period,
            'totals': data['totals'],
        }
        fullpath = generate_mfs(data, 'publisher')['fullpath']

        # redirect
        url = reverse_lazy('mailing:new', args=[publisher.pk])  # base url
        query_string = urlencode({
            'filename': fullpath,
            'on_fail': referer})
        url = '{}?{}'.format(url, query_string)
        return url
