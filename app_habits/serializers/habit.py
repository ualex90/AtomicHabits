from rest_framework import serializers

from app_habits.models import Habit
from validators.general_validators import FillingNotOutTwoFieldsValidator
from app_habits.validators.habit import (
    TimeToCompleteValidator,
    RelatedHabitOnlyNiceValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitNiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('start_time', 'periodicity', 'related_habit', 'reward')
        read_only_fields = ('owner', 'is_nice')
        validators = [
            # Проверяем что время выполнения не превышает 120 секунд
            TimeToCompleteValidator('time_to_complete'),
        ]


class HabitGoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner', 'is_nice')
        validators = [
            # Проверяем что одновременно не указаны связанная привычка и вознаграждение
            FillingNotOutTwoFieldsValidator('related_habit', 'reward'),
            # Проверяем что время выполнения не превышает 120 секунд
            TimeToCompleteValidator('time_to_complete'),
            # Проверяем что в связанных привычках, привычка с признаком приятной
            RelatedHabitOnlyNiceValidator('related_habit'),
        ]


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice')


class HabitListAllSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()

    @staticmethod
    def get_owner_email(instance):
        owner_email = instance.owner.email
        return owner_email

    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
