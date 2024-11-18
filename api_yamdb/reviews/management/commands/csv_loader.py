import csv
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comments, Genre, TitleGenre,
                            Review, Title)
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Импорт информации из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь до CSV-файла')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            try:
                if 'category' in csv_file_path:
                    for row in csv_reader:
                        Category.objects.create(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                elif 'comments' in csv_file_path:
                    for row in csv_reader:
                        Comments.objects.create(
                            id=row['id'],
                            review_id=row['review_id'],
                            text=row['text'],
                            author_id=row['author'],
                            pub_date=row['pub_date'],
                        )
                elif 'genre_title' in csv_file_path:
                    for row in csv_reader:
                        TitleGenre.objects.create(
                            id=row['id'],
                            title_id=row['title_id'],
                            genre_id=row['genre_id'],
                        )
                elif 'genre' in csv_file_path:
                    for row in csv_reader:
                        Genre.objects.create(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                elif 'review' in csv_file_path:
                    for row in csv_reader:
                        Review.objects.create(
                            id=row['id'],
                            title_id=row['title_id'],
                            text=row['text'],
                            author_id=row['author'],
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                elif 'title' in csv_file_path:
                    for row in csv_reader:
                        Title.objects.create(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category_id=row['category'],
                        )
                elif 'user' in csv_file_path:
                    for row in csv_reader:
                        CustomUser.objects.create_user(
                            id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                        )
                else:
                    print('Не найдено модели для данных!')
            except ValidationError as error:
                print(f'Ошибка при создании объекта: {error}')
            except IntegrityError as e:
                print(f'Не возможно загрузить данные, ошибка: {e}')
