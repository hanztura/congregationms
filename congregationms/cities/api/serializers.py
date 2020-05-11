from rest_framework import serializers

from cities.models import Country, State, City


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'symbol']


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'symbol', 'country', 'country_id']


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'symbol', 'state', 'state_id']
