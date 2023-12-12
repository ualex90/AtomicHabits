from django.urls import reverse
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_users.models import User


class HabitTest(APITestCase):

    def setUp(self):
        # User_1
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.nice_habit_1 = Habit.objects.create(
            task="Test nice habit 1",
            location="Test location 1",
            is_nice=True,
            owner=self.user_1
        )

        self.good_habit_1 = Habit.objects.create(
            task="Test good habit 1",
            location="Test location 1",
            is_nice=False,
            related_habit=self.nice_habit_1,
            owner=self.user_1
        )

        self.good_habit_2 = Habit.objects.create(
            task="Test good habit 2",
            location="Test location 2",
            is_nice=False,
            reward="Test reward 1",
            is_public=True,
            owner=self.user_1
        )

        # User_2
        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        self.nice_habit_2 = Habit.objects.create(
            task="Test nice habit 2",
            location="Test location 2",
            is_nice=True,
            is_public=True,
            owner=self.user_2
        )

        self.good_habit_3 = Habit.objects.create(
            task="Test good habit 3",
            location="Test location 3",
            is_nice=False,
            related_habit=self.nice_habit_2,
            owner=self.user_2
        )

        self.good_habit_4 = Habit.objects.create(
            task="Test good habit 4",
            location="Test location 4",
            is_nice=False,
            reward="Test reward 2",
            owner=self.user_2
        )

        # Moderator
        self.moderator = User.objects.create(
            email="moderator@test.com",
            is_staff=True,
            is_active=True,
        )
        self.moderator.set_password('test')
        self.moderator.save()

    def test_list_for_user(self):
        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse("app_habits:habit_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.nice_habit_1.id,
                        'task': 'Test nice habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': True
                    },
                    {
                        'id': self.good_habit_1.id,
                        'task': 'Test good habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': False
                    },
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False
                    }
                ]
            }
        )

    def test_list_for_moderator(self):
        # Аутентифицируем модератора
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            reverse("app_habits:habit_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 6,
                'next': 'http://testserver/habit/list/?page=2',
                'previous': None,
                'results': [
                    {
                        'id': self.nice_habit_1.id,
                        'task': 'Test nice habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.good_habit_1.id,
                        'task': 'Test good habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.nice_habit_2.id,
                        'task': 'Test nice habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user2@test.com'
                    },
                    {
                        'id': self.good_habit_3.id,
                        'task': 'Test good habit 3',
                        'start_time': None,
                        'location': 'Test location 3',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user2@test.com'
                    }
                ]
            }
        )

    def test_public_list(self):

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse("app_habits:habit_public_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.nice_habit_2.id,
                        'task': 'Test nice habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user2@test.com'
                    }
                ]
            }
        )

    def test_destroy(self):
        """ Тестирование удаления """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем привычку
        habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        # считаем количество привычек в базе данных до удаления
        count_habit_1 = Habit.objects.all().count()

        # Изменяем привычку
        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': habit.id})
        )

        # считаем количество привычек в базе данных после удаления
        count_habit_2 = Habit.objects.all().count()

        self.assertTrue(
            count_habit_1 - 1 == count_habit_2
        )
