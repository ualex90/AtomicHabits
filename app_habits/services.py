import json
from datetime import datetime, date, time

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from app_habits.models import Habit


def add_task(habit: Habit):
    """ Создание периодической задачи для напоминания о полезной привычке """

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        name=f'{habit.id}: {habit.task}',
        task='app_habits.task.send_message',
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
