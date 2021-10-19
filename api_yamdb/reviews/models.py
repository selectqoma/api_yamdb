import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Avg, UniqueConstraint
from django.core.exceptions import ValidationError

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
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории',
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
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры',
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
        verbose_name='Категрия'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )

    name = models.CharField(
        verbose_name='Название',
        max_length=256)
    year = models.PositiveIntegerField()

    @property
    def rating(self):
        score = self.reviews.filter(
            title=self
        ).aggregate(Avg('score'))
        return score['score__avg']

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тайтл',
        verbose_name_plural = 'Тайтлы',
        ordering = ('-year',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.year > dt.datetime.today().year:
            raise ValidationError('Неверный год')
        super().save(*args, **kwargs)


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
        verbose_name='Текст',
        validators=[MaxLengthValidator(90000, message='Превышен лимит знаков')]
    )
    score = models.PositiveIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Оценка',

    )
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_review'
            )
        ]

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
        verbose_name = 'Коментарий',
        verbose_name_plural = 'Коментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:50]
