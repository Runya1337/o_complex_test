import json
from pathlib import Path
from django.core.management.base import BaseCommand
from weather.models import City

class Command(BaseCommand):
    help = 'Load a list of cities into the database'

    def handle(self, *args, **options):
        # Путь к файлу JSON
        path_to_json = Path(__file__).resolve().parent / 'bd_json' / 'cities.json'

        with open(path_to_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            cities = data['city'] 

            for city in cities:
                city_id = city['city_id']
                name = city['name']
                City.objects.update_or_create(
                    city_id=city_id,
                    defaults={
                        'name': name,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded cities into the database'))
