from rest_framework import serializers

from app_habits.models import Habit
from validators.general_validators import FillingNotOutTwoFieldsValidator
from app_habits.validators.habit import TimeToCompleteValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitNiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('start_time', 'periodicity', 'related_habit', 'reward')
        read_only_fields = ('owner', 'is_nice_habit')
        validators = []


class HabitGoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner', 'is_nice_habit')
        validators = [
            # Проверяем что одновременно не указаны связанная привычка и вознаграждение
            FillingNotOutTwoFieldsValidator('related_habit', 'reward'),
            TimeToCompleteValidator('time_to_complete'),
        ]


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('task', 'start_time', 'location', 'periodicity', 'is_nice_habit')

