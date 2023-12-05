from django.urls import path

from app_habits.apps import AppHabitsConfig
from app_habits.views.habit import (
    HabitNiceCreateAPIView,
    HabitGoodCreateAPIView,
    HabitListAPIView,
)

name = AppHabitsConfig.name

urlpatterns = [
    path('habit/create/nice/', HabitNiceCreateAPIView.as_view(), name="habit_nice_create"),
    path('habit/create/good/', HabitGoodCreateAPIView.as_view(), name="habit_good_create"),
    path('habit/list/', HabitListAPIView.as_view(), name="habit_list"),
]
