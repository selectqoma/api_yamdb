import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

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
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        blank=True,
        default='без жанра'
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
    )

    class Meta:
        ordering = ('name',)

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
        related_name='titles',
        blank=True,
    )

    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(
            dt.datetime.today().year, message='Неверная дата'), ]
    )

    @property
    def rating(self):
        score = self.reviews.filter(
            title=self
        ).aggregate(Avg('score'))
        return score['score__avg']

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модлель для обзоров."""
    SCORE_CHOICES = [
        (i, i) for i in range(1, 11)
    ]
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Тайтл'

    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст отзыва',
        validators=[MaxLengthValidator(90000, message='Превышен лимит знаков')]
    )
    score = models.PositiveIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='оценка',

    )
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """Модель для комментариев."""
    review = models.ForeignKey(
        Review,
        verbose_name='Обзор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE,

    )
    text = models.TextField(
        'Текст комментария',
        validators=[MaxLengthValidator(
            2000,
            message='Превышен лимит знаков')]
    )
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:50]
