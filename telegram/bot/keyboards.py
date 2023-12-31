from aiogram import types

main = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main.add(types.KeyboardButton(text="Подписаться на прогноз погоды 📆 \n(или обновить данные)"))
main.add(types.KeyboardButton(text="Отменить подписку ❎"))


weather_format = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
weather_format.add(
    types.InlineKeyboardButton(text="Текстовое уведомление 🆎"),
    types.KeyboardButton(text="Табличка csv 🗓️"),
    types.KeyboardButton(text='Отмена ❌'),
)

weather_location = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
weather_location.add(
    types.KeyboardButton(text="Отправить геолокацию 🕹", request_location=True),
    types.KeyboardButton(text="Назад ◀️"),
    types.KeyboardButton(text='Отмена ❌'),
)
