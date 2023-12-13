from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
)

from app_habits.models import Habit
from app_habits.paginators.habit import HabitPaginator
from app_habits.serializers.habit import (
    HabitGoodCreateSerializer,
    HabitNiceCreateSerializer,
    HabitListSerializer,
    HabitListAllSerializer, HabitSerializer,
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
      (для админа, дополнительно owner_email)
    """

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = None
    filterset_fields = ('is_nice', )
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
        else:
            serializer_class = HabitListSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', )

        return serializer_class


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Подробный просмотр привычки
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitPublicListAPIView(ListAPIView):
    """
    Получение списка публичных привычек.
    - Доступна фильтрация по признаку приятной привычки
      is_nice (true, false)
    - Сортировка по любому доступному полю
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitListAllSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
    filterset_fields = ('is_nice', )
    pagination_class = HabitPaginator


class HabitUpdateAPIView(UpdateAPIView):
    """ Изменение привычки """

    queryset = Habit.objects.all()

    def get_serializer_class(self):
        if self.get_object().is_nice:
            return HabitNiceCreateSerializer
        return HabitGoodCreateSerializer


class HabitDestroyAPIView(DestroyAPIView):
    """ Удаление привычки """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
