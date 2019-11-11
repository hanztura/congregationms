

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
from .utils import (compute_month_year, generate_mfs,
                    get_mfs_data, get_months_and_years)
from publishers.models import Publisher, Group
from system.utils import LoginAndPermissionRequiredMixin


now = datetime.now().date()


class MFSList(LoginAndPermissionRequiredMixin, ListView):
    """MFS stands for Month Field Service."""
    model = MonthlyFieldService
    permission_required = 'reports.view_monthlyfieldservice',

    def get_queryset(self):
        default_month_year = compute_month_year(now)
        monthyear = self.request.GET.get('monthyear', default_month_year)
        monthyear = monthyear.split('-')
        year = monthyear[0]
        month = monthyear[1]
        return MonthlyFieldService.objects.filter(
            month_ending__year=year,
            month_ending__month=month
        )

    def get_context_data(self, **kwargs):
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


class MFSCreate(LoginAndPermissionRequiredMixin, CreateView):
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


class MFSUpdate(LoginAndPermissionRequiredMixin, UpdateView):
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
        context['totals'] = context['reports'].aggregate(
            Sum('placements'),
            Sum('video_showing'),
            Sum('hours'),
            Sum('return_visits'),
            Sum('bible_study'))

        view_type = self.kwargs['view_type']  # publisher or group

        if view_type == 'publisher':
            publisher = self.kwargs['publisher']
            publisher = Publisher.objects.get(slug=publisher)
            context['publisher'] = publisher
        else:
            group = self.kwargs['group']
            group = Group.objects.get(pk=group)
            context['group'] = group

        # date from and date to
        date_from = self.request.GET.get('from', str(now))
        date_to = self.request.GET.get('to', str(now))

        dates = get_months_and_years(date_from, date_to)

        context['from'] = dates['df']
        context['to'] = dates['dt']
        return context

    def get_queryset(self):
        view_type = self.kwargs['view_type']  # publisher or group

        date_from = self.request.GET.get('from', str(now))
        date_to = self.request.GET.get('to', str(now))

        date_from = date_from.split('-')
        date_to = date_to.split('-')

        from_month, from_year = date_from[1], date_to[0]
        to_month, to_year = date_to[1], date_to[0]

        if view_type == 'publisher':
            publisher = self.kwargs['publisher']
            publisher = Publisher.objects.get(slug=publisher)

            queryset = MonthlyFieldService.objects.filter(
                publisher=publisher,
                month_ending__month__gte=from_month,
                month_ending__year__gte=from_year
            )
        else:
            group = self.kwargs['group']
            group = Group.objects.get(pk=group)

            queryset = MonthlyFieldService.objects.filter(
                group=group,
                month_ending__month__gte=from_month,
                month_ending__year__gte=from_year
            )

        queryset = queryset.filter(
            month_ending__month__lte=to_month,
            month_ending__year__lte=to_year
        )
        queryset = queryset.order_by(
            '-month_ending', 'publisher__last_name', 'publisher__first_name')

        return queryset


@login_required
@permission_required('reports.view_monthlyfieldservice', raise_exception=True)
def sample_mfs(request, pk):
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
