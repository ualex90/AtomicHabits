import requests
from django.core.management import BaseCommand

from app_habits.task import send_message
from config import settings


class MyBot:
    URL = "https://api.telegram.org/bot"
    TOKEN = settings.TELEGRAM_BOT_TOKEN

    def send_message(self, text, chat_id=None):
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': '361991641',
                'text': text
            }
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_message()
