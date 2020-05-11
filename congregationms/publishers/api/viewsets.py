import datetime

from rest_framework import viewsets

from .serializers import GroupSerializer
from publishers.models import Group


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # filter allowed groups only
        allowed_groups = self.request.authorized_groups
        allowed_groups = [g.group_id for g in allowed_groups]  # Group.id
        queryset = queryset.filter(id__in=allowed_groups)

        return queryset
