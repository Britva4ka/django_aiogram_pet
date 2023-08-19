from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherSub(StatesGroup):
    format = State()
    location = State()
