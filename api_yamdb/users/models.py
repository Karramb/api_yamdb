from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from enum import Enum


class UserRoles(Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    @classmethod
    def choices(cls):
        return tuple((attribute.name, attribute.value) for attribute in cls)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя содержит недопустимые символы'
        )],
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=16,
        choices=UserRoles.choices(),
        default=UserRoles.user.name,
        verbose_name='Роль'

    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
