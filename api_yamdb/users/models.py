from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class User(AbstractUser):

    USER_ROLES = [
            (ADMIN, 'Администратор'),
            (MODERATOR, 'Модератор'),
            (USER, 'Пользователь'),
        ]

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )

    bio = models.TextField(
        verbose_name='Описание',
        max_length=500,
        blank=True,
    )

    role = models.CharField(
        max_length=10,
        verbose_name='Тип пользователя',
        choices=USER_ROLES,
        default=USER,
    )

    confirmation_code = models.UUIDField(
        verbose_name='Код подтверждения',
        default=uuid.uuid4,
        editable=False,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
