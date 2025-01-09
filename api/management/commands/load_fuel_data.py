import csv
from django.core.management.base import BaseCommand
from api.models import FuelStation

class Command(BaseCommand):
    help = 'Load fuel station data from CSV'

    def handle(self, *args, **kwargs):
        with open('fuel_prices.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                FuelStation.objects.create(
                    name=row['Truckstop Name'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    retail_price=row['Retail Price'],
                )
        self.stdout.write(self.style.SUCCESS('Fuel data loaded successfully'))
