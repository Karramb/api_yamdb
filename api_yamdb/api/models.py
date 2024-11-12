from django.db import models


class Category(models.Model):
    """Категории."""

    name = models.CharField(max_length=256)
    slug = models.CharField(r'^[-a-zA-Z0-9_]+$', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр."""

    name = models.CharField(max_length=256)
    slug = models.CharField(r'^[-a-zA-Z0-9_]+$', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(max_length=256)
    # этот тип выбрала т к у него значения от 0 до 32767.
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='categories', null=True
    )

    def __str__(self):
        return self.name
