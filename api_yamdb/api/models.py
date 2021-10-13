import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )
    slug = models.SlugField(
        'Slug',
        unique=True
    )

    class Meta:
        ordering = ('slug',)


class Genre(models.Model):
    slug = models.SlugField(
        'Slug',
        unique=True
    )

    class Meta:
        ordering = ('slug',)


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    name = models.CharField('Название', max_length=50)
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(
            dt.datetime.today().year, message='Неверная дата'), ]
    )

    class Meta:
        ordering = ('-year',)
