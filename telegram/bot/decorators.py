from functools import wraps
from aiogram import types, Dispatcher
from .utils import delete_last_message
import logging


def delete_last_messages(func):
    """
    Decorator for deleting last bot message and user message.
    Only for message handlers
    :param func: handler link
    :return: Delete last bot message and last user message
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        # Удаление последнего сообщения бота
        await delete_last_message(message)

        result = await func(message, *args, **kwargs)
        # Удаление сообщения пользователя
        await message.delete()

        return result

    return wrapper


def finish_any_state(func):
    """
    Decorator for finishing any state.
    For example: u can use it for /cancel
    :param func:
    :return: Finish state
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        dp = Dispatcher.get_current()
        state = dp.current_state(user=message.from_user.id)
        current_state = await state.get_state()
        if current_state:
            logging.info('Cancelling state %r', current_state)
            await state.finish()
        result = await func(message, *args, **kwargs)

        return result

    return wrapper
