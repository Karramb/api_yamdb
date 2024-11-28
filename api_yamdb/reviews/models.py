import datetime as dt

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.abstracts import NameSlugModel, ObjectBaseModel
from reviews.constants import LOOK_TEXT, MAX_LEN_TEXT, MAX_SCORE, MIN_SCORE


def validate_year(value):
    now_year = dt.datetime.now().year
    if value > now_year:
        raise ValidationError(
            f'Год выпуска {value} не может быть больше текущего {now_year}.'
        )
    return value


class Category(NameSlugModel):

    class Meta(NameSlugModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):

    class Meta(NameSlugModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_LEN_TEXT)
    year = models.SmallIntegerField('Год', validators=[validate_year])
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, verbose_name='Категория'
    )

    class Meta:
        ordering = ('name', 'year')
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return f'{self.name[:LOOK_TEXT]=}, {self.year=}, {self.description=}'


class Review(ObjectBaseModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение')
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MinValueValidator(MIN_SCORE),
                              MaxValueValidator(MAX_SCORE)]
    )

    class Meta(ObjectBaseModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author',
            ),
        )

    def __str__(self):
        return f'{self.title}, {self.score}'


class Comment(ObjectBaseModel):
    text = models.TextField('Текст')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ObjectBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LOOK_TEXT]
