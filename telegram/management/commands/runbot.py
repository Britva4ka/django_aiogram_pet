from django.core.management.base import BaseCommand
from telegram.bot.main import main


class Command(BaseCommand):
    help = 'Запускает телеграм-бота'

    def handle(self, *args, **options):
        main()
