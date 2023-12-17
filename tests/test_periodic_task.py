import json

from django.urls import reverse
from django_celery_beat.models import PeriodicTask
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_habits.services import send_message_to_telegram
from app_users.models import User


class PeriodicTaskTest(APITestCase):

    def setUp(self):
        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            telegram_id="123456789",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        # Nice Habit
        self.nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1
        )

    def test_periodic_task_simple(self):
        """
        Тестирование создания периодической задачи
        без вознаграждения и связанной привычки
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "start_time": "12:10",
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        task = PeriodicTask.objects.get(name=f'{response.json().get("id")}: {data["task"]}')

        # Проверяем что задача создана
        self.assertTrue(
            task
        )

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            json.loads(task.kwargs),
            {
                'telegram_id': "123456789",
                'start_time': '12:10',
                'task': 'Test task good',
                'location': 'Test location',
                'time_to_complete': 60,
                'reward': None,
                'related_habit': None
            }
        )

    def test_message_simple(self):
        """
        Тестирование формирование сообщения из периодической задачи
        """

        kwargs = {
            'telegram_id': "123456789",
            'start_time': '12:10',
            'task': 'Test task good',
            'location': 'Test location',
            'time_to_complete': 60,
            'reward': None,
            'related_habit': None
        }

        message = send_message_to_telegram(**kwargs)

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            message,
            'Я буду Test task good в 12:10 Test location в течении 60 секунд.'
        )

    def test_periodic_task_reward(self):
        """
        Тестирование создания периодической задачи
        с вознаграждением
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "start_time": "12:10",
            "reward": "Test reward"
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        task = PeriodicTask.objects.get(name=f'{response.json().get("id")}: {data["task"]}')

        # Проверяем что задача создана
        self.assertTrue(
            task
        )

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            json.loads(task.kwargs),
            {
                'telegram_id': "123456789",
                'start_time': '12:10',
                'task': 'Test task good',
                'location': 'Test location',
                'time_to_complete': 60,
                'reward': 'Test reward',
                'related_habit': None
            }
        )

    def test_message_reward(self):
        """
        Тестирование формирование сообщения из периодической задачи
        """

        kwargs = {
            'telegram_id': "123456789",
            'start_time': '12:10',
            'task': 'Test task good',
            'location': 'Test location',
            'time_to_complete': 60,
            'reward': 'Test reward',
            'related_habit': None
        }

        message = send_message_to_telegram(**kwargs)

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            message,
            'Я буду Test task good в 12:10 Test location в течении 60 секунд.\n'
            'За это, я Test reward.'

        )

    def test_periodic_task_related_habit(self):
        """
        Тестирование создания периодической задачи
        со связанной привычкой
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "start_time": "12:10",
            "related_habit": self.nice_habit.id
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        task = PeriodicTask.objects.get(name=f'{response.json().get("id")}: {data["task"]}')

        # Проверяем что задача создана
        self.assertTrue(
            task
        )

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            json.loads(task.kwargs),
            {
                'telegram_id': "123456789",
                'start_time': '12:10',
                'task': 'Test task good',
                'location': 'Test location',
                'time_to_complete': 60,
                'reward': None,
                'related_habit': {
                    'task': 'Test nice habit',
                    'location': 'Test location',
                    'time_to_complete': 60
                }
            }
        )

    def test_message_related_habit(self):
        """
        Тестирование формирование сообщения из периодической задачи
        """

        kwargs = {
            'telegram_id': "123456789",
            'start_time': '12:10',
            'task': 'Test task good',
            'location': 'Test location',
            'time_to_complete': 60,
            'reward': None,
            'related_habit': {
                'task': 'Test nice habit',
                'location': 'Test location',
                'time_to_complete': 60
            }
        }

        message = send_message_to_telegram(**kwargs)

        # Проверяем содержимое именованных аргументов
        self.assertEquals(
            message,
            'Я буду Test task good в 12:10 Test location в течении 60 секунд.\n'
            'После этого я Test nice habit Test location в течении 60 секунд.'
        )
