import csv
import glob
import os

from django.db import IntegrityError
from django.http.response import Http404
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (Category, Comments, Genre, TitleGenre,
                            Review, Title)
from users.models import CustomUser
from reviews.constants import PATH


MODELS_DICT = {
    'category': Category,
    'comments': Comments,
    'genre_title': TitleGenre,
    'genre': Genre,
    'review': Review,
    'title': Title,
    'user': CustomUser,
}


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
        path += '*.csv'
        files = []
        for filename in glob.glob(os.path.join(path)):
            files.append(filename)

        return files

    def get_model(self, filename):
        for file in MODELS_DICT:
            if file in filename:
                return MODELS_DICT[file]

    def handle(self, *args, **kwargs):
        files = self.load_file(PATH)

        for filename in files:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)

                    model = self.get_model(filename)
                    data = []

                    try:
                        if model:
                            for row in csv_reader:
                                row = self.change_title(row)
                                data.append(model(**row))
                        else:
                            self.stdout.write(
                                f'Не найдена модель для {filename}!')

                        model.objects.bulk_create(data, ignore_conflicts=True)
                    except Http404:
                        files.append(filename)
                    except IntegrityError:
                        files.append(filename)
                self.stdout.write('Загрузка завершена!')
            except FileNotFoundError:
                self.stdout.write('Файл не найден!')
