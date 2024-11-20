import csv
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from reviews.constants import MODELS_DICT


class Command(BaseCommand):
    help = 'Импорт информации из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь до CSV-файла')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            model = None

            try:
                for el in MODELS_DICT:
                    if el in csv_file_path:
                        model = MODELS_DICT[el]
                        break

                if model:
                    for row in csv_reader:
                        model.objects.create(**row)
                else:
                    print('Не найдена модель!')
            except ValidationError as error:
                print(f'Ошибка при создании объекта: {error}')
            except IntegrityError as e:
                print(f'Не возможно загрузить данные, ошибка: {e}')
