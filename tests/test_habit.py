from django.urls import reverse
from rest_framework.test import APITestCase

from app_users.models import User


class HabitNiceTest(APITestCase):

    def SetUp(self):

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
        response = self.client.post(
            reverse("app_habits:habit_nice_create")
        )