import json

from django.core.management.base import BaseCommand

from foodgram_backend.settings import IMPORT_FILES_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных из json.'

    def handle(self, *args, **kwargs):
        with open(
            f'{IMPORT_FILES_DIR}/ingredients.json',
            'r',
            encoding='UTF-8'
        ) as file:
            Ingredient.objects.bulk_create(
                Ingredient(**row)
                for row in json.loads(file.read())
            )
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
