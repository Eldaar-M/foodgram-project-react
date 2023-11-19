import json

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка тегов в базу данных из json.'

    def handle(self, *args, **kwargs):
        with open(
                '{CSV_FILES_DIR}/tags.json', 'r',
                encoding='UTF-8'
        ) as ingredients:
            ingredient_data = json.loads(ingredients.read())
            for ingredients in ingredient_data:
                Tag.objects.get_or_create(**ingredients)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
