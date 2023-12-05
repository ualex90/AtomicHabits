from rest_framework import serializers


class TimeToCompleteValidator:
    """ Проверка, что время выполнения не превышает максимальное время"""

    def __init__(self, field, max_time=120):
        self.field = field
        self.max_time = max_time

    def __call__(self, value):
        if int(dict(value).get(self.field)) > self.max_time:
            raise serializers.ValidationError(f"Время выполнения задания не "
                                              f"должно превышать {self.max_time} секунд")
