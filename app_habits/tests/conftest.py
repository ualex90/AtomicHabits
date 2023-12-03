import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from app_users.models import User


@pytest.fixture
def user_1():
    user = User.objects.create(
        email="user1@test.com",
        is_staff=False,
        is_active=True,
    )
    return user


@pytest.fixture
def simple_user_1_client(user_1):
    client = APIClient()

    refresh = RefreshToken.for_user(user_1)
    access_token = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client
