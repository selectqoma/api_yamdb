from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import uuid

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class UserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        if not email:
            raise ValueError('Введите адрес электронной почты')
        if not username:
            raise ValueError('Введите имя пользователя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Введите адрес электронной почты')
        if not username:
            raise ValueError('Введите имя пользователя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role='admin',
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):

    USER_ROLES = [
            (ADMIN, 'Администратор'),
            (MODERATOR, 'Модератор'),
            (USER, 'Пользователь'),
        ]

    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
        blank=False,
        null=False
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True,
        null=True
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

    def is_moderator(self):
        return self.role == 'moderator'

    def is_admin(self):
        return self.role == 'admin'

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
