import pytz
import datetime
from timezonefinder import TimezoneFinder
from aiogram import Dispatcher, Bot, types

import logging

WEATHER_EMOJIS = {
    "clear sky": "🌞",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "🌥️",
    "overcast clouds": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "smoke": "🌫️",
    "sand/dust whirls": "💨",
    "haze": "🌫️",
    "volcanic ash": "🌋",
    "squalls": "🌪️",
    "tornado": "🌪️",
    "drizzle": "🌧️",
    "light intensity drizzle": "🌧️",
    "heavy intensity drizzle": "🌧️",
    "light intensity drizzle rain": "🌧️",
    "drizzle rain": "🌧️",
    "heavy intensity drizzle rain": "🌧️",
    "shower rain and drizzle": "🌧️",
    "heavy shower rain and drizzle": "🌧️",
    "shower drizzle": "🌧️",
    "light rain": "🌧️",
    "moderate rain": "🌧️",
    "heavy intensity rain": "🌧️🌧️",
    "very heavy rain": "🌧️🌧️",
    "extreme rain": "🌧️🌧️",
    "freezing rain": "🌧️❄️",
    "light intensity shower rain": "🌧️",
    "shower rain": "🌧️",
    "heavy intensity shower rain": "🌧️🌧️",
    "ragged shower rain": "🌧️",
    "snow": "❄️",
    "light snow": "❄️",
    "heavy snow": "❄️❄️",
    "sleet": "🌨️",
    "shower sleet": "🌨️",
    "light rain and snow": "🌧️❄️",
    "rain and snow": "🌧️❄️",
    "light shower snow": "🌨️",
    "shower snow": "🌨️",
    "heavy shower snow": "🌨️❄️",
    "thunderstorm": "⛈️",
    "thunderstorm with light rain": "⛈️🌧️",
    "thunderstorm with rain": "⛈️🌧️",
    "thunderstorm with heavy rain": "⛈️🌧️",
    "light thunderstorm": "⛈️",
    "heavy thunderstorm": "⛈️",
    "ragged thunderstorm": "⛈️",
    "thunderstorm with light drizzle": "⛈️🌧️",
    "thunderstorm with drizzle": "⛈️🌧️",
    "thunderstorm with heavy drizzle": "⛈️🌧️",
}
tf = TimezoneFinder()


def translate_to_emoji(status) -> str:
    """
    translate text string to emoji string
    :param status: weather status
    :return: emoji
    """
    status = status.lower()
    return WEATHER_EMOJIS.get(status, status)


def get_str_timezone_by_coordinates(latitude, longitude):
    tz_str = tf.timezone_at(lng=longitude, lat=latitude)
    return tz_str


def get_object_timezone_by_str(tz_str):
    timezone = pytz.timezone(tz_str)
    return timezone


def get_current_time_by_timezone(timezone):
    current_time = datetime.datetime.now(timezone)
    return current_time


async def delete_last_message(message: types.Message):
    dp = Dispatcher.get_current()
    bot = Bot.get_current()
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()
    last_msg = data.get('last_msg')
    if last_msg is not None:
        await bot.delete_message(chat_id=message.chat.id, message_id=last_msg)
    else:
        logging.info("Last bot message not found")
