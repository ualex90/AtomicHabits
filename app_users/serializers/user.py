from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app_users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя

    Выполняется проверка введения пароля
    """

    password_again = serializers.CharField(
        max_length=128,
        label=_("Password (again)"),
        write_only=True
    )

    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password_again = self.validated_data['password_again']
        # Проверяем совпадают ли пароли
        if password != password_again:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({'detail': "Введенные пароли не совпадают"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'password_again', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }
