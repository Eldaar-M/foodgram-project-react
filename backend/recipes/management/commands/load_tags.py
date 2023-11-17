import csv

from django.core.management.base import BaseCommand

from foodgram_backend.settings import CSV_FILES_DIR
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных'

    def handle(self, *args, **kwargs):
        with open(
            f'{CSV_FILES_DIR}/tags.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            tags = [
                Tag(
                    name=row[0],
                    slug=row[1],
                    color=row[2],
                )
                for row in reader
            ]
            Tag.objects.bulk_create(tags)
