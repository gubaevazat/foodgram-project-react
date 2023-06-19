import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load data from json'

    def handle(self, *args, **options):

        load_dir = settings.BASE_DIR.parent / 'data'
        with open(
            load_dir / 'ingredients.json',
            'r', encoding='utf-8'
        ) as json_file:
            data = json.load(json_file)
            Ingredient.objects.bulk_create(
                [Ingredient(
                    name=value['name'],
                    measurement_unit=value['measurement_unit']
                ) for value in data],
                batch_size=200
            )
