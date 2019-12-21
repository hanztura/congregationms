from rest_framework import viewsets

from .serializers import MFSSerializer
from reports.models import MonthlyFieldService


class MFSViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonthlyFieldService.objects.all()
    serializer_class = MFSSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        group = self.request.query_params.get('group', None)
        if group:
            queryset = queryset.filter(group=group)

        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from:
            queryset = queryset.filter(month_ending__gte=date_from)

        if date_to:
            queryset = queryset.filter(month_ending__lte=date_to)

        return queryset
