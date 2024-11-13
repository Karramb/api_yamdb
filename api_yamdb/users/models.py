from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = (
    ('User', 'Пользователь'),
    ('Moderator', 'Модератор'),
    ('Admin', 'Администратор')
)


class CustomUser(AbstractUser):
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE,
        default=ROLE[0],
        verbose_name='Роль'

    )

    def __str__(self):
        return self.username
