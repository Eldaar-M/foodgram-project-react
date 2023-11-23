import csv

from django.core.management.base import BaseCommand

from foodgram_backend.settings import IMPORT_FILES_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных из csv.'

    def handle(self, *args, **kwargs):
        with open(
            f'{IMPORT_FILES_DIR}/ingredients.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            Ingredient.objects.bulk_create([
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ])
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
