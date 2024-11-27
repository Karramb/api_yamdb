from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    EMAIL_MAX_LENGTH,
    MAX_LENGTH_FOR_FIELDS
)
from users.validators import username_validate


class YaMDBUser(AbstractUser):
    class UserRoles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        unique=True,
        validators=[username_validate],
        verbose_name='Никнейм',
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=max(len(choice) for choice, _ in UserRoles.choices),
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        blank=True,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        blank=True,
        verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == self.UserRoles.ADMIN
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR
