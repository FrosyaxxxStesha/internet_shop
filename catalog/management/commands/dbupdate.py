from django.core.management.base import BaseCommand
from os import system


class Command(BaseCommand):
    help = 'очищает базу данных и заполняет её данными из файла фикстуры'

    def handle(self, *args, **options):
        system(f'python manage.py flush --no-input')
        system(f'python manage.py loaddata {options["fixture_name"]}')

    def add_arguments(self, parser):
        parser.add_argument(
            'fixture_name',
            nargs='?',
            type=str,
            default='data.json'
        )

