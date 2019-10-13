from datetime import datetime

from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import MonthlyFieldService


now = datetime.now().date()


class MFSList(ListView):
    """
    MFS stands for Month Field Service.
    """
    model = MonthlyFieldService

    def get_queryset(self):
        month = self.request.GET.get('month', now.month)
        year = self.request.GET.get('year', now.year)
        return MonthlyFieldService.objects.filter(
            month_ending__year=year,
            month_ending__month=month
        )


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
