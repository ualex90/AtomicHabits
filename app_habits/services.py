import json
from datetime import datetime, date, time

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from app_habits.models import Habit
from config import settings


class TgBot:
    URL = "https://api.telegram.org/bot"
    TOKEN = settings.TELEGRAM_BOT_TOKEN

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def send_message(self, text):
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': self.chat_id,
                'text': text
            }
        )


def add_task(habit: Habit):
    """ Создание периодической задачи для напоминания о полезной привычке """

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        name=f'{habit.id}: {habit.task}',
        task='app_habits.tasks.send_message_tg',
        interval=schedule,
        kwargs=json.dumps(
            {
                'telegram_id': habit.owner.telegram_id,
                'start_time': time.strftime(habit.start_time, '%H:%M'),
                'task': habit.task,
                'location': habit.location,
                'reward': habit.reward,
            }, ensure_ascii=False
        ),
        start_time=datetime.combine(date.today(), habit.start_time),
    )


def send_message_to_telegram(*args, **kwargs):
    print(kwargs)
    chat_id = kwargs.get('telegram_id')
    text = 'Message'
    tg_bot = TgBot(chat_id)
    tg_bot.send_message(text)
