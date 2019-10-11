from datetime import datetime

from django.views.generic import DetailView, ListView

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
