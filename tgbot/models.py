from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name='Telegram ID')
    username = models.CharField(max_length=255, null=True, verbose_name='Telegram username')
    first_name = models.CharField(max_length=255, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return f'{self.first_name} {self.last_name} (@{self.username} id{self.id}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['created_at']


class UserLocation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'id{self.user_id}: ({self.latitude}, {self.longitude})'

    class Meta:
        verbose_name = "Локация пользователя"
        verbose_name_plural = "Локации пользователей"
        ordering = ['created_at']


class Pub(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=300, null=True, blank=True, default='Название', verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес')
    place_type = models.CharField(max_length=300, null=True, blank=True, verbose_name='Тип заведение')
    social_media_link = models.CharField(max_length=300, null=True, blank=True, verbose_name='Соцсеть')
    working_hours = models.CharField(max_length=300, null=True, blank=True, verbose_name='Рабочие часы')
    photo = models.ImageField(upload_to="media/", null=True, blank=True, verbose_name='Фотография')
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True,)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True,)
    city = models.CharField(max_length=300, null=True, blank=True, verbose_name='Город', default='Санкт-Петербург')
    ymaps = models.CharField(max_length=300, null=True, blank=True, verbose_name='Yandex Maps')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return f'{self.name} - {self.address}'

    class Meta:
        verbose_name = "Заведение"
        verbose_name_plural = "Заведения"
        ordering = ['created_at']



