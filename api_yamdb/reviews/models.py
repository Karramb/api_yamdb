from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator
)

from users.models import CustomUser


class CommentReviewBaseModel(models.Model):
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField('Текст')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = 'pub_date',


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Имя содержит недопустимые символы')],
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Имя содержит недопустимые символы')],
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField('Год')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='categories', null=True, verbose_name='Категория'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(CommentReviewBaseModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        blank=True, verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta(CommentReviewBaseModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author',
            ),
        )

    def __str__(self):
        return f'{self.title.name}, {self.score}'


class Comments(CommentReviewBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(CommentReviewBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:10]
