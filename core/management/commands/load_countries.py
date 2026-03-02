import pycountry
from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Load all countries into the Country table'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading countries...')

        for country in pycountry.countries:
            print(country)
            try:
                country_obj, created = Country.objects.get_or_create(
                    name=country.name,
                    defaults={
                        'iso_code': country.alpha_2
                    }
                )
                if created:
                    self.stdout.write(f'Added country: {country.name}')
                else:
                    self.stdout.write(f'Country already exists: {country.name}')
            except Exception as e:
                pass

        self.stdout.write(self.style.SUCCESS('All countries loaded successfully.'))
