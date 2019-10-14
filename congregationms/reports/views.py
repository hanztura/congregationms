from datetime import datetime

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import MonthlyFieldService
from .utils import compute_month_year
from publishers.models import Publisher


now = datetime.now().date()


class MFSList(ListView):
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


class MFSDelete(DeleteView):
    model = MonthlyFieldService
    success_url = reverse_lazy('reports:mfs-index')

    def get_success_url(self):
        message = "Successfully deleted."
        messages.success(self.request, message)
        return super().get_success_url()


class MFSDetail(DetailView):
    model = MonthlyFieldService
    context_object_name = 'report'


class MFSCreate(CreateView):
    model = MonthlyFieldService
    fields = [
        'publisher',
        'month_ending',
        'placements',
        'video_showing',
        'hours',
        'return_visits',
        'bible_study',
        'comments'
    ]

    def form_valid(self, form):
        messages.success(
            self.request,
            'Successfully created new Monthly Field Service Report.'
        )
        return super().form_valid(form)


class MFSUpdate(UpdateView):
    model = MonthlyFieldService
    fields = [
        'publisher',
        'month_ending',
        'placements',
        'video_showing',
        'hours',
        'return_visits',
        'bible_study',
        'comments'
    ]
    context_object_name = 'report'


class MFSHistoryList(ListView):
    model = MonthlyFieldService
    template_name = 'reports/mfs_publisher_history.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publisher = self.kwargs['publisher']
        publisher = Publisher.objects.get(pk=publisher)
        context['publisher'] = publisher
        return context

    def get_queryset(self):
        publisher = self.kwargs['publisher']
        publisher = Publisher.objects.get(pk=publisher)

        date_from = self.request.GET.get('from', now)
        date_to = self.request.GET.get('to', now)

        queryset = MonthlyFieldService.objects.filter(
            publisher=publisher,
            month_ending__gte=date_from
        )
        queryset = queryset.filter(month_ending__lte=date_to)
        return queryset
