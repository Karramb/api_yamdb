import csv
import glob
import os

from django.db import IntegrityError
from django.http.response import Http404
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category
from users.models import CustomUser
from reviews.constants import MODELS_DICT, PATH


class Command(BaseCommand):
    help = 'Импорт информации из CSV-файла'

    def change_title(self, row):
        if 'author' in row:
            row['author'] = get_object_or_404(
                CustomUser, pk=row['author']
            )
        elif 'category' in row:
            row['category'] = get_object_or_404(
                Category, pk=row['category']
            )
        return row

    def load_file(self, path):
        files = []
        for filename in glob.glob(os.path.join(path)):
            files.append(filename)

        return files

    def handle(self, *args, **kwargs):
        files = self.load_file(PATH)
        for filename in files:
            with open(filename, 'r', encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                model = None

                for el in MODELS_DICT:
                    if el in filename:
                        model = MODELS_DICT[el]
                        break

                if model:
                    try:
                        for row in csv_reader:
                            row = self.change_title(row)
                            model.objects.get_or_create(**row)
                    except Http404:
                        files.append(filename)
                    except IntegrityError as e:
                        if 'FOREIGN KEY constraint failed' in str(e):
                            files.append(filename)
                        else:
                            print(f'Невозможно загрузить данные '
                                  f'из файла {filename}, '
                                  f'ошибка: {e}')
                else:
                    print(f'Не найдена модель для {filename}!')

        print('Загрузка завершена!')
