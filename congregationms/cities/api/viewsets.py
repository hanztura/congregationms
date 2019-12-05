from rest_framework import viewsets

from .serializers import CitySerializer, CountrySerializer, StateSerializer
from cities.models import City, Country, State


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country=country)

        return queryset


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(state=state)

        return queryset
