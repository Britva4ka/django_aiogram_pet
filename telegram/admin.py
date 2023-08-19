from django.contrib import admin
from .models import TelegramUser, WeatherSubscription
# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(WeatherSubscription)
