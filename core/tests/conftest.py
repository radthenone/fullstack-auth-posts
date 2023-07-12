from tests.users.factories import UserFactory
import pytest
from rest_framework.authtoken.models import Token


@pytest.fixture
def create_user(db, django_user_model):
    user = UserFactory.build()
    return django_user_model.objects.create_user(
        username=user.username,
        email=user.email,
        password=user.password,
    )


@pytest.fixture
def get_or_create_token(db, create_user):
    token, _ = Token.objects.get_or_create(user=create_user)
    return token


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def auth_client(api_client, create_user, get_or_create_token):
    api_client.force_authenticate(user=create_user, token=get_or_create_token)
    return api_client
