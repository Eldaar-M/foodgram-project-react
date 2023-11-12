from csv import reader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных'

    def handle(self, *args, **kwargs):
        with open('data/ingredients.csv',
                  'r',
                  encoding='UTF-8'
                  ) as ingredients:
            for name, unit in reader(ingredients):
                try:
                    Ingredient.objects.get_or_create(name=name,
                                                     measurement_unit=unit)
                except Exception as error:
                    print(error)
