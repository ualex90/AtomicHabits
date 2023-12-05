from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView
)

from app_habits.models import Habit
from app_habits.paginators.habit import HabitPaginator
from app_habits.serializers.habit import (
    HabitGoodCreateSerializer,
    HabitNiceCreateSerializer,
    HabitListSerializer,
)


class HabitNiceCreateAPIView(CreateAPIView):
    """ Создание приятной привычки """

    serializer_class = HabitNiceCreateSerializer

    def perform_create(self, serializer):
        new_habit = serializer.save()

        new_habit.owner = self.request.user  # Добавляем пользователя
        new_habit.is_nice = True  # Устанавливаем признак приятной привычки

        new_habit.save()


class HabitGoodCreateAPIView(CreateAPIView):
    """ Создание полезной привычки """

    serializer_class = HabitGoodCreateSerializer

    def perform_create(self, serializer):
        new_habit = serializer.save()

        new_habit.owner = self.request.user  # Добавляем пользователя

        new_habit.save()


class HabitListAPIView(ListAPIView):
    """
    Получение списка привычек.
    - Доступна фильтрация по признаку приятной привычки
      is_nice (true, false)
    - Сортировка по любому доступному полю
    """

    queryset = Habit.objects.all()
    serializer_class = HabitListSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('task', 'start_time', 'location', 'periodicity', 'is_nice')
    filterset_fields = ('is_nice',)
    pagination_class = HabitPaginator
