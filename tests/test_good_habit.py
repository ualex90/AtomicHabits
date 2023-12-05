from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_users.models import User


class HabitGoodTest(APITestCase):

    def setUp(self):

        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        self.user_3 = User.objects.create(
            email="user3@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_3.set_password('test')
        self.user_3.save()

        # Nice Habit
        self.nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice_habit=True,
            owner=self.user_1
        )

    def test_create(self):
        """ Тестирование создания объекта с минимальным набором полей """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем ответ
        self.assertEquals(
            response.json(),
            {
                "id": response.json().get("id"),
                "task": "Test task good",
                "start_time": None,
                "location": "Test location",
                "is_nice_habit": False,
                "periodicity": "1",
                "reward": None,
                "time_to_complete": 60,
                "is_public": False,
                "owner": self.user_1.id,
                "related_habit": None
            }
        )

    def test_filling_not_out_two_fields_validator(self):
        """
        Тестирование валидатора FillingOutTwoFieldsValidator
        при одновременном указании связанной привычки и вознаграждения
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "related_habit": self.nice_habit.id,
            "reward": "Test reward"
        }

        response = self.client.post(
            reverse("app_habits:habit_good_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Недопустимо одновременно указывать "related_habit" и "reward"']}
        )
