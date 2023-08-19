import logging
import asyncio
import random
import aiocron
from django.conf import settings
from ..models import TelegramUser
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .database import WeatherSubscriptionManager, add_new_user, format_translater
from .utils import get_object_timezone_by_str, get_current_time_by_timezone
from .decorators import delete_last_messages, finish_any_state
from .services import ForecastManager
from .states import WeatherSub
from .middlewares import ThrottlingMiddleware, SaveLastMessageMiddleware
from . import keyboards as kb

API_TOKEN = settings.TELEGRAM_BOT_API_TOKEN
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize storage, bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
fm = ForecastManager()
wsm = WeatherSubscriptionManager()

# Setup middlewares
dp.middleware.setup(LoggingMiddleware())  # logging
dp.middleware.setup(ThrottlingMiddleware(limit=2))  # anti-flood
dp.middleware.setup(SaveLastMessageMiddleware())  # remember last bot message id (handler must return msg object)


@dp.message_handler(commands=['admin'], state='*')
@delete_last_messages
@finish_any_state
async def admin_panel(message: types.Message) -> types.Message:
    """
    Заготовка под админ панель
    """
    pass


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo(message: types.Message):
    """
    Developer handler to use images
    """
    user = TelegramUser.objects.filter(telegram_id=message.from_user.id).afirst()
    if user.is_admin:
        # chat_id = developer id. You can make field in db for this if there are more than one dev. But I don't
        await bot.send_photo(chat_id=int(settings.TG_DEV_ID),
                             photo=message.photo[-1].file_id,
                             caption=message.photo[-1].file_id
                             )


@dp.message_handler(commands=['start'], state='*')
@delete_last_messages
@finish_any_state
async def send_welcome(message: types.Message) -> types.Message:
    """
    Bot Start Handler
    Add user info to database
    Give user main keyboard
    """
    sent_message = await message.answer_photo(
        photo="AgACAgIAAxkBAAIJCWTchytn2IhLSnRyENtU-W0B4q5gAAI5yzEbm_zhSliItVQvSMuWAQADAgADeAADMAQ",
        caption='Привет!\nЯ бот-питомец Britva4ka!🇺🇦\nУмею разное, выбирай в меню',
        reply_markup=kb.main
    )
    # sent_message = await message.answer("Привет!\nЯ бот-питомец Britva4ka!🇺🇦\n"
    #                                     "Умею разное, выбирай в меню", reply_markup=kb.main)
    await add_new_user(message)
    return sent_message


@dp.message_handler(commands=['help'], state='*')
@delete_last_messages
@finish_any_state
async def help_handler(message: types.Message) -> types.Message:
    """
    Help
    """
    sent_message = await message.answer(text="Возникли вопросы? Пиши @Britva4ka ")
    return sent_message


@dp.message_handler(commands=['menu', 'cancel'], state='*')
@dp.message_handler(Text(contains=['отмена'], ignore_case=True), state="*")
@delete_last_messages
@finish_any_state
async def menu(message: types.Message) -> types.Message:
    """
    Main menu.
    Cancel any action, give user main keyboard
    """
    sent_message = await message.answer(text='Главное меню.', reply_markup=kb.main)
    return sent_message


@dp.message_handler(Text(contains="Отменить подписку", ignore_case=True), state=None)
@delete_last_messages
async def cancel_subscription(message: types.Message) -> types.Message:
    any_sub = False
    markup = types.InlineKeyboardMarkup()
    if await wsm.exists(message.from_user.id):
        any_sub = True
        markup.add(types.InlineKeyboardButton(text="Погода", callback_data='weather'))
    if any_sub:
        markup.add(types.InlineKeyboardButton(text="Отмена", callback_data='cancel'))
        sent_message = await message.answer(text="Выберите подписку, которую хотите отменить", reply_markup=markup)
    else:
        sent_message = await message.answer(text="У вас нет ни одной подписки", reply_markup=kb.main)
    return sent_message


@dp.callback_query_handler()
async def delete_subscription(call: types.CallbackQuery):
    sent_message = None
    if call.data == 'weather':
        await wsm.delete(user_id=call.from_user.id)
        sent_message = await call.message.answer(text='Успешно', reply_markup=kb.main)
    elif call.data == 'cancel':
        sent_message = await call.message.answer(text='Отмена', reply_markup=kb.main)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    return sent_message


@dp.message_handler(Text("Подписаться на прогноз погоды 📆 \n(или обновить данные)"), state=None)
@delete_last_messages
async def start_weather_sub(message: types.Message) -> types.Message:
    """
    Initialize weather subscription
    Gives user keyboard for choosing notification format
    """
    sent_message = await message.answer(text="Выберите формат уведомлений:", reply_markup=kb.weather_format)
    await WeatherSub.format.set()
    return sent_message


@dp.message_handler(lambda message: message.text not in ['Текстовое уведомление 🆎', 'Табличка csv 🗓️'],
                    state=WeatherSub.format)
@delete_last_messages
async def check_format(message: types.Message) -> types.Message:
    """
    If user sending not correct format
    """
    sent_message = await message.answer('Не корректный формат. Воспользуйся кнопкой.',
                                        reply_markup=kb.weather_format)
    return sent_message


@dp.message_handler(Text(equals=['Текстовое уведомление 🆎', 'Табличка csv 🗓️']), state=WeatherSub.format)
@delete_last_messages
async def set_weather_format(message: types.Message, state: FSMContext) -> types.Message:
    """
    Weather subscription, step 2
    Gives user kb for sending location
    """
    sent_message = await message.answer('Отправьте вашу геолокацию', reply_markup=kb.weather_location)
    await state.update_data(format=message.text)
    await WeatherSub.next()
    return sent_message


@dp.message_handler(Text(contains=['назад'], ignore_case=True), state=WeatherSub.location)
@delete_last_messages
async def back_to_format(message: types.Message) -> types.Message:
    """
    Back button handler (if user want to change format pick)
    Gives back kb for choosing notification format
    """
    sent_message = await message.answer(text="Выберите формат уведомлений", reply_markup=kb.weather_format)
    await WeatherSub.previous()
    return sent_message


@dp.message_handler(lambda message: not message.location, state=WeatherSub.location)
@delete_last_messages
async def check_location(message: types.Message) -> types.Message:
    """
    If user sending not a location
    """
    sent_message = await message.answer('Это не геолокация. Воспользуйся кнопкой.',
                                        reply_markup=kb.weather_location)
    return sent_message


@dp.message_handler(content_types=[types.ContentType.LOCATION], state=WeatherSub.location)
@delete_last_messages
async def save_user_location(message: types.Message, state: FSMContext):
    """
    Function for saving user's coordinates.
    """
    sent_message = await message.answer("Подписка завершена!\n"
                                        "Теперь в 7 утра по твоему часовому поясу будешь получать прогноз на сутки 😇\n"
                                        "Можешь выбрать еще что-то, я разное умею 😏", reply_markup=kb.main)
    data = await state.get_data()
    weather_format = format_translater[data['format']]
    await wsm.create(message, weather_format)
    await state.finish()
    return sent_message


@dp.message_handler()
async def echo(message: types.Message) -> None:
    """
    Unexpected messages handler
    """
    phrases = ["Ого, что это за шифровка? 🤔",
               "Моя искусственная интеллектуальность не понимает вашего сообщения 🧠",
               "Упс, что-то пошло не так... 🙃",
               "Ты что, меня троллишь? 😅"]
    await message.reply(random.choice(phrases))


# TODO Кнопку чтобы получить текущую погоду (если нет локации в базе - запросить город).
# TODO Курсы валют same.
# Функция для отправки уведомления о погоде в 7:00 по часовому поясу пользователя
async def send_forecast_to_user(user_id, latitude, longitude, forecast_format) -> None:
    """
    Send forecast to user
    """
    location = [float(latitude), float(longitude)]
    if forecast_format == 'txt':

        message = fm.create_message(*location)
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except BotBlocked:
            logging.info(f"User has {user_id} blocked the bot.")

    elif forecast_format == 'csv':

        csv_file = fm.create_csv(*location)
        try:
            await bot.send_document(chat_id=user_id, document=types.InputFile(csv_file, "weather_data.csv"))
        except BotBlocked:
            logging.info(f"User has {user_id} blocked the bot.")


async def send_weather_notifications() -> None:
    """
    Sent forecast to subscribed users every day.
    """
    weather_subscriptions = await wsm.get_all()
    for weather_sub in weather_subscriptions:
        timezone = get_object_timezone_by_str(weather_sub.timezone)
        current_time = get_current_time_by_timezone(timezone)
        if True:  # DEBUG
        # if current_time.hour == 7 and current_time.minute == 0:
            data = {
                "user_id": weather_sub.telegram_user.telegram_id,
                "longitude": weather_sub.longitude,
                "latitude": weather_sub.latitude,
                "forecast_format": weather_sub.format
                }
            asyncio.create_task(send_forecast_to_user(**data))
    logging.info(f"Weather notifications sent")


def main():
    # Запуск бота та завдання для щоденного надсилання погоди
    loop = asyncio.get_event_loop()
    aiocron.crontab('* * * * *', func=send_weather_notifications, loop=loop)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
