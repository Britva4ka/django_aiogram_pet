from abc import ABC, abstractmethod
from aiogram import types
from asgiref.sync import sync_to_async


class SubscriptionManager(ABC):
    """
    Remember that all operations with database in aiogram context
    should be done asynchronous
    """
    @staticmethod
    @abstractmethod
    @sync_to_async  # <--- this is "must have" decorator
    def get_all():
        pass

    @staticmethod
    @abstractmethod
    @sync_to_async
    def create(message: types.Message, weather_format: str):
        pass

    @staticmethod
    @abstractmethod
    @sync_to_async
    def exists(user_id: int):
        pass

    @staticmethod
    @abstractmethod
    @sync_to_async
    def delete(user_id: int):
        pass
