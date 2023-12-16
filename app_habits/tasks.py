from celery import shared_task

from app_habits.models import Habit
from app_habits.services import send_message_to_telegram


@shared_task
def print_task():
    pass


@shared_task
def send_message_tg(*args, **kwargs):
    # print(kwargs)
    send_message_to_telegram(*args, **kwargs)
