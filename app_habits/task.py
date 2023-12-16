from celery import shared_task

from app_habits.models import Habit


@shared_task
def create_periodic_task():
    pass


def send_message(*args, **kwargs):
    print("РАБОТАЮ !!!!!")
