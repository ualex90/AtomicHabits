from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_users.models import User


class HabitNiceTest(APITestCase):

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

    def test_create(self):
        """ Тестирование создания объекта с минимальным набором полей """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task nice",
            "location": "Test location",
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
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
                "task": "Test task nice",
                "location": "Test location",
                "is_nice_habit": True,
                "time_to_complete": 60,
                "is_public": False,
                "owner": self.user_1.id
            }
        )
