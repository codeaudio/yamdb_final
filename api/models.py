import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .config import ADMIN, MODER, USER
from .models_validator import username_validator, year_validator


class CustomUser(AbstractUser):
    username = models.CharField(
        unique=True,
        verbose_name='username',
        max_length=30,
        validators=[username_validator]
    )
    email = models.EmailField(
        unique=True,
        verbose_name='адрес почты'
    )
    bio = models.CharField(
        null=True,
        max_length=150,
        blank=True,
        verbose_name='Информация',
    )
    first_name = models.CharField(
        null=True,
        max_length=35,
        blank=True,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        null=True,
        max_length=35,
        blank=True,
        verbose_name='Фамилия пользователя',
    )
    password = models.CharField(
        null=True,
        max_length=90,
        blank=True,
        verbose_name='Пароль пользователя',
    )
    confirmation_code = models.TextField(
        null=True,
        blank=True,
        verbose_name='Код подтверждения',
    )

    class Role(models.TextChoices):
        USER = USER, USER
        MODERATOR = MODER, MODER
        ADMIN = ADMIN, ADMIN

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('role', 'username', 'password')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moder(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_user(self):
        return self.role == self.Role.USER


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        default=uuid.uuid1,
        verbose_name='Адрес URL жанра',
    )

    class Meta:
        db_table = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        default=uuid.uuid1,
        verbose_name='Адрес URL категории',
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год публикации',
        validators=[year_validator]

    )
    description = models.TextField(
        verbose_name='Описание произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория произведения',
    )

    class Meta:
        db_table = 'title'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Обзор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор обзора',
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MaxValueValidator(
                10,
                '10 is max value'
            ),
            MinValueValidator(
                1,
                '10 is min value'
            )
        ]
    )

    class Meta:
        db_table = 'review'
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ['-pub_date']
        constraints = [
            UniqueConstraint(fields=['title', 'author'], name='uniq')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор произведения',
    )

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.author
