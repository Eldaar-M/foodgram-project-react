import csv

from django.core.management.base import BaseCommand

from foodgram_backend.settings import IMPORT_FILES_DIR
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка тегов в базу данных из csv.'

    def handle(self, *args, **kwargs):
        with open(
            f'{IMPORT_FILES_DIR}/tags.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            Tag.objects.bulk_create([
                Tag(
                    name=row[0],
                    slug=row[1],
                    color=row[2],
                )
                for row in reader
            ])
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
