from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView
)

from app_habits.models import Habit
from app_habits.paginators import HabitPaginator
from app_habits.serializers.habit import (
    HabitGoodCreateSerializer,
    HabitNiceCreateSerializer,
    HabitListSerializer,
)


class HabitNiceCreateAPIView(CreateAPIView):
    serializer_class = HabitNiceCreateSerializer


class HabitGoodCreateAPIView(CreateAPIView):
    serializer_class = HabitGoodCreateSerializer


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.filter(is_nice_habit=True)
    serializer_class = HabitListSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('task', 'start_time', 'location', 'periodicity', 'is_nice_habit')
    filterset_fields = ('is_nice_habit',)
    pagination_class = HabitPaginator
