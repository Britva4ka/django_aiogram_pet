from aiogram import types
from telegram.models import TelegramUser, WeatherSubscription
from .abstractions import SubscriptionManager
from .utils import get_str_timezone_by_coordinates
from asgiref.sync import sync_to_async

ALLOWED_FORMATS = ['txt', 'csv']
format_translater = {
    'Текстовое уведомление 🆎': "txt",
    'Табличка csv 🗓️': "csv",
    }


async def add_new_user(message: types.Message):  # made just to show the another way to use db without sync_to_async
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user = await TelegramUser.objects.filter(telegram_id=user_id).afirst()
    if not user:
        user = await TelegramUser.objects.acreate(telegram_id=user_id,
                                                  username=username,
                                                  first_name=first_name,
                                                  last_name=last_name)
    return user


def add_new_user_sync(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user = TelegramUser.objects.filter(telegram_id=user_id).first()
    if not user:
        user = TelegramUser.objects.create(telegram_id=user_id,
                                           username=username,
                                           first_name=first_name,
                                           last_name=last_name)
    return user


class WeatherSubscriptionManager(SubscriptionManager):
    @staticmethod
    @sync_to_async
    def get_all():
        weather_subs = WeatherSubscription.objects.select_related('telegram_user').all()
        return [weather_sub for weather_sub in weather_subs]

    @staticmethod
    @sync_to_async
    def create(message: types.Message, weather_format: str):
        if weather_format not in ALLOWED_FORMATS:
            raise Exception("Not allowed format")
        user_id = message.from_user.id
        latitude = message.location.latitude
        longitude = message.location.longitude
        timezone = get_str_timezone_by_coordinates(latitude, longitude)
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        if not user:
            user = add_new_user_sync(message)
        weather_sub = WeatherSubscription.objects.filter(telegram_user=user).first()
        if not weather_sub:  # create
            weather_sub = WeatherSubscription.objects.create(
                telegram_user=user,
                format=weather_format,
                latitude=latitude,
                longitude=longitude,
                timezone=timezone
            )
        else:  # edit
            weather_sub.format = weather_format
            weather_sub.latitude = latitude
            weather_sub.longitude = longitude
            weather_sub.timezone = timezone
            weather_sub.save()
        return weather_sub

    @staticmethod
    @sync_to_async
    def exists(user_id: int):
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        weather_sub = WeatherSubscription.objects.filter(telegram_user=user).first()
        return weather_sub is not None

    @staticmethod
    @sync_to_async
    def delete(user_id: int):
        user = TelegramUser.objects.filter(telegram_id=user_id).first()
        sub = WeatherSubscription.objects.filter(telegram_user_id=user.id).first()
        if sub:
            sub.delete()
