# Generated by Django 4.1.6 on 2023-10-03 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Название', max_length=300, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес')),
                ('place_type', models.CharField(blank=True, max_length=300, null=True, verbose_name='Тип заведение')),
                ('social_media_link', models.CharField(blank=True, max_length=300, null=True, verbose_name='Соцсеть')),
                ('working_hours', models.CharField(blank=True, max_length=300, null=True, verbose_name='Рабочие часы')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Фотография')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('city', models.CharField(blank=True, default='Санкт-Петербург', max_length=300, null=True, verbose_name='Город')),
                ('ymaps', models.CharField(blank=True, max_length=300, null=True, verbose_name='Yandex Maps')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'Заведение',
                'verbose_name_plural': 'Заведения',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Telegram ID')),
                ('username', models.CharField(max_length=255, null=True, verbose_name='Telegram username')),
                ('first_name', models.CharField(max_length=255, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, null=True, verbose_name='Фамилия')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['created_at'],
            },
        ),
    ]
