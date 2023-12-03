from rest_framework.generics import CreateAPIView

from app_habits.serializers.habit import HabitCreateSerializer


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitCreateSerializer
