import json
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from cities.models import Country, State, City


class Command(BaseCommand):
    help = 'Set up Philippine states and cities'

    @transaction.atomic
    def handle(self, *args, **options):
        # get or create Philippines
        print('Setting up Philippines...')
        ph, created = Country.objects.get_or_create(name='Philippines')
        current_path = os.path.dirname(os.path.abspath(__file__))

        # get or create States
        print('Setting up states...')
        filename = 'data/philippines/refregion.json'
        filename = os.path.join(current_path, filename)
        with open(filename) as f:
            data = json.load(f)

        for state in data['RECORDS']:
            import_code = state['regCode']
            name = state['regDesc']

            state, created = State.objects.get_or_create(
                country=ph,
                name=name,
                symbol=import_code,
                import_code=import_code
            )

            if created:
                msg = 'created state: {}'.format(str(state))
                print(msg)

        # get or create Cities
        print('Setting up cities...')
        filename = 'data/philippines/refcitymun.json'
        filename = os.path.join(current_path, filename)
        with open(filename) as f:
            data = json.load(f)

        for city in data['RECORDS']:
            name = city['citymunDesc']
            symbol = city['citymunCode']
            reg_code = city['regDesc']

            state = State.objects.get(import_code=reg_code, country=ph)

            city, created = City.objects.get_or_create(
                name=name,
                symbol=symbol,
                state=state
            )

            if created:
                msg = 'created city: {}'.format(str(city))
                print(msg)
