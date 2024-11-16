from django.db import models

# from users.models import CustomUser


class Category(models.Model):
    """Категории."""

    name = models.CharField(max_length=256)
    slug = models.CharField(r'^[-a-zA-Z0-9_]+$', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр."""

    name = models.CharField(max_length=256)
    slug = models.CharField(r'^[-a-zA-Z0-9_]+$', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(max_length=256)
    # этот тип выбрала т к у него значения от 0 до 32767.
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='categories', null=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Связь произведения и жанров."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Reviews(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', blank=True)
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField(null=True)
    # author = models.ForeignKey(
    #     CustomUser, related_name='reviews', on_delete=models.CASCADE,
    # )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('pub_date', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=['author',],
                name='unique_follow',
            ),
        ]

    def __str__(self):
        return f'{self.title.name}, {self.score}'


class Comments(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='comments'
    # )
    author = models.IntegerField(null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'коментарии'
        ordering = ('pub_date', 'id')

    def __str__(self):
        return self.text[:10]
