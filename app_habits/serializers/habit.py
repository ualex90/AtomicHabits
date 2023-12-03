from rest_framework import serializers

from app_habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = []


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('task', 'start_time', 'location', 'periodicity',)


