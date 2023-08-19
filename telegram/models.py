from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
FORMATS_CHOICES = [
    ("txt", "Текстовое уведомление"),
    ("csv", "Табличка CSV"),
]


User = get_user_model()


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='tg_user', null=True, blank=True)
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        db_table = 'telegram_user'
        verbose_name = 'Telegram Пользователь'
        verbose_name_plural = 'Telegram Пользователи'
        ordering = ['username']


class WeatherSubscription(models.Model):
    telegram_user = models.OneToOneField(TelegramUser, on_delete=models.SET_NULL, related_name='weather_sub',
                                         null=True, blank=True)
    timezone = models.CharField(max_length=64)
    format = models.CharField(max_length=5, choices=FORMATS_CHOICES, default="txt")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.telegram_user} weather subscription'

    class Meta:
        db_table = 'telegram_weather_subscription'
        verbose_name = 'Подписка на погоду'
        verbose_name_plural = 'Подписки на погоду'
        ordering = ['telegram_user']
