from django.db import models

from reviews.constants import MAX_LEN_SLUG, MAX_LEN_TEXT
from users.models import YaMDBUser


class NameSlugModel(models.Model):
    name = models.CharField('Название', max_length=MAX_LEN_TEXT)
    slug = models.SlugField('Слаг', max_length=MAX_LEN_SLUG, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class ContentBaseModel(models.Model):
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField('Текст')
    author = models.ForeignKey(
        YaMDBUser, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='%(class)s_objectbase'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)ss'
