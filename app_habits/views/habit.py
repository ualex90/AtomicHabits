from django.db.models import QuerySet
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
    HabitListAllSerializer,
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
      is_nice (true, false) для обычного пользователя
      и дополнительно 'owner_email' для модератора
    - Сортировка по любому доступному полю
    """

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = None
    filterset_fields = None
    pagination_class = HabitPaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Habit.objects.all()
        else:
            queryset = Habit.objects.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            serializer_class = HabitListAllSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
            self.filterset_fields = ('is_nice', 'owner_email', )
        else:
            serializer_class = HabitListSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', )
            self.filterset_fields = ('is_nice', )

        return serializer_class


class HabitPublicListAPIView(ListAPIView):
    """
    Получение списка публичных привычек.
    - Доступна фильтрация по признаку приятной привычки
      is_nice (true, false) и 'owner_email'
    - Сортировка по любому доступному полю
    """

    queryset = Habit.objects.filter(is_public=True)
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = None
    filterset_fields = None
    pagination_class = HabitPaginator

    def get_serializer_class(self):
        serializer_class = HabitListAllSerializer
        self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
        self.filterset_fields = ('is_nice', 'owner_email', )

        return serializer_class
