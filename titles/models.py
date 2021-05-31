from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR)
    )

    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(choices=ROLES, max_length=20, default=USER)
    conformation_code = models.CharField(max_length=10, blank=True)

    class Meta:

        verbose_name = 'user'
        verbose_name_plural = 'users'

        ordering = ['username']


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    # __dir__ - было странной опечаткой...
    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False, db_index=True,
    )
    year = models.IntegerField(
        validators=[validate_year],
        blank=True, db_index=True,
    )
    description = models.TextField(
        max_length=500,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True, db_index=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True, db_index=True,
        related_name='titles')

    class Meta:
        ordering = ['name']
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """
    Модель для отзывов

    text - текст отзыва
    author - автор
    title - произведение, к которому написан отзыв
    score - рейтинг отзыва
    pub_date - дата публикации
    """
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        default=10,
        validators=[
            MinValueValidator(0, 'Values out the range from 1 to 10'),
            MaxValueValidator(10, 'Values out the range from 1 to 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'revies'
        ordering = ['pub_date']
        unique_together = ('author', 'title')


class Comment(models.Model):
    """
    Модель для комментариев

    text - текст комментария
    author - автор
    review - отзыв, к которому был написан комментарий
    pub_date - дата публикации
    """
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['pub_date']
