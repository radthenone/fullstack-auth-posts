import uuid

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


class TestUser:
    def __init__(self, username=None, email=None, password=None):
        self.username = username or str(uuid.uuid4())
        self.email = email or self.username + "@example.com"
        self.password = password or "test-password"


@pytest.fixture
def create_user(db, django_user_model):
    user = TestUser()
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


@pytest.mark.django_db
class TestUsersClient:
    def test_users(self, auth_client, get_or_create_token):
        url = reverse("user-list")
        response = auth_client.get(
            url, format="json", HTTP_AUTHORIZATION="Token " + get_or_create_token.key
        )
        assert response.status_code == 200
