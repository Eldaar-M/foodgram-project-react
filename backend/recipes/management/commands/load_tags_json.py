import json

from django.core.management.base import BaseCommand

from foodgram_backend.settings import IMPORT_FILES_DIR
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка тегов в базу данных из json.'

    def handle(self, *args, **kwargs):
        with open(
                f'{IMPORT_FILES_DIR}/tags.json', 'r',
                encoding='UTF-8'
        ) as file:
            reader = json.loads(file.read())
            Tag.objects.bulk_create([
                Tag(
                    name=row['name'],
                    slug=row['slug'],
                    color=row['color'],
                )
                for row in reader
            ])
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
