import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MFSForm
from .models import MonthlyFieldService
from .utils import compute_month_year, generate_mfs
from publishers.models import Publisher, Group


now = datetime.now().date()


class MFSList(LoginRequiredMixin, ListView):
    """
    MFS stands for Month Field Service.
    """
    model = MonthlyFieldService


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


class MFSDelete(LoginRequiredMixin, DeleteView):
    model = MonthlyFieldService
    success_url = reverse_lazy('reports:mfs-index')

    def get_success_url(self):
        message = "Successfully deleted."
        messages.success(self.request, message)
        return super().get_success_url()


class MFSDetail(LoginRequiredMixin, DetailView):
    model = MonthlyFieldService
    context_object_name = 'report'


class MFSCreate(LoginRequiredMixin, CreateView):
    model = MonthlyFieldService
    form_class = MFSForm

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully created new Monthly Field Service Report.'
        )
        return super().form_valid(form)


class MFSUpdate(LoginRequiredMixin, UpdateView):
    model = MonthlyFieldService
    form_class = MFSForm
    context_object_name = 'report'


class MFSHistoryList(LoginRequiredMixin, ListView):
    model = MonthlyFieldService
    template_name = 'reports/mfs_history.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        date_from = date_from.split('-')
        date_to = date_to.split('-')

        date_from = '{}-{}'.format(date_from[0], date_from[1])
        date_to = '{}-{}'.format(date_to[0], date_to[1])

        context['from'] = date_from
        context['to'] = date_to
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
        queryset = queryset.order_by('-month_ending', 'publisher__last_name', 'publisher__first_name')

        return queryset


@login_required
def sample_mfs(request, pk):
    date_from = request.GET.get('from', str(now))
    date_to = request.GET.get('to', str(now))

    date_from = date_from.split('-')
    date_to = date_to.split('-')

    from_month, from_year = date_from[1], date_to[0]
    to_month, to_year = date_to[1], date_to[0]

    queryset = MonthlyFieldService.objects.filter(
        month_ending__month__gte=from_month,
        month_ending__year__gte=from_year
    )
    queryset = queryset.filter(
        month_ending__month__lte=to_month,
        month_ending__year__lte=to_year
    )

    _from = '{}-{}'.format(from_month, from_year)
    _to = '{}-{}'.format(to_month, to_year)

    group = Group.objects.get(pk=pk)
    queryset = queryset.order_by('-month_ending', 'publisher__last_name', 'publisher__first_name')
    queryset = [q for q in queryset if q.publisher.group == group]

    congregation = str(group.congregation)
    group = group.name
    month = '{} to {}'.format(_from, _to)

    data = {
        'queryset': queryset,
        'group': group,
        'congregation': congregation,
        'month': month
    }
    s = '/home/hanz/projects/congregationms/media/{}.docx'.format(str(uuid.uuid1()))
    doc = generate_mfs(data)
    doc.save(s)
    return FileResponse(open(s, 'rb'), as_attachment=True, filename='download.docx')
