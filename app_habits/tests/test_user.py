from django.conf import settings


def test_user(user_1):
    settings.configure()
    print(user_1)
