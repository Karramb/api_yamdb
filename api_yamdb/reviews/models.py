import datetime as dt
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from reviews.constants import LOOK_TXT, MAX_LEN_SLUG, MAX_LEN_TXT

def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего.'
        )


class BaseModel(models.Model):
    name = models.CharField('Название', max_length=MAX_LEN_TXT)
    slug = models.SlugField('Слаг', max_length=MAX_LEN_SLUG, unique=True)

    class Meta:
        abstract=True
        ordering = ('name',)

    def __str__(self):
        return self.name

class Category(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=MAX_LEN_TXT)
    year = models.SmallIntegerField('Год', validators=[validate_year])
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', related_name='genres'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='categories', null=True, verbose_name='Категория'
    )

    class Meta:
        ordering = ('name', 'year')
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class CommentReviewBaseModel(models.Model):
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True) 
    text = models.TextField('Текст') 
    author = models.ForeignKey( 
        CustomUser, on_delete=models.CASCADE, 
        verbose_name='Автор' 
    ) 

    class Meta:
        abstract=True
        ordering = ('-pub_date',)
    

class Review(CommentReviewBaseModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        blank=True, verbose_name='Произведение')
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
    text = models.TextField('Комментарий')
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
        return self.text[:LOOK_TXT]
