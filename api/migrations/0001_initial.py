# Generated by Django 3.2.3 on 2021-11-08 01:54

import uuid

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import api.models_validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, validators=[api.models_validator.username_validator], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='адрес почты')),
                ('bio', models.CharField(blank=True, max_length=150, null=True, verbose_name='Информация')),
                ('first_name', models.CharField(blank=True, max_length=35, null=True, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(blank=True, max_length=35, null=True, verbose_name='Фамилия пользователя')),
                ('password', models.CharField(blank=True, max_length=90, null=True, verbose_name='Пароль пользователя')),
                ('confirmation_code', models.TextField(blank=True, null=True, verbose_name='Код подтверждения')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=9, verbose_name='Роль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'user',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True, verbose_name='Адрес URL категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название жанра')),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True, verbose_name='Адрес URL жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'genre',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название произведения')),
                ('year', models.IntegerField(validators=[api.models_validator.year_validator], verbose_name='Год публикации')),
                ('description', models.TextField(verbose_name='Описание произведения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='titles', to='api.category', verbose_name='Категория произведения')),
                ('genre', models.ManyToManyField(related_name='titles', to='api.Genre', verbose_name='Жанр произведения')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'db_table': 'title',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Обзор')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10, '10 is max value'), django.core.validators.MinValueValidator(1, '10 is min value')], verbose_name='Оценка произведения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор обзора')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.title', verbose_name='Название произведения')),
            ],
            options={
                'verbose_name': 'Обзор',
                'verbose_name_plural': 'Обзоры',
                'db_table': 'review',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.review', verbose_name='Обзор произведения')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'comment',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='uniq'),
        ),
    ]
