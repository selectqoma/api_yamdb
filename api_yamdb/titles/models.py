import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    """Модель для категории."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель для тайтлов."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )

    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(
            dt.datetime.today().year, message='Неверная дата'), ]
    )

    rating = models.PositiveIntegerField(verbose_name='Рейтинг')
    description = models.TextField()

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name
