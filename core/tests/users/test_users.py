import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUsersClient:
    @pytest.mark.usefixtures("auth_client", "get_or_create_token")
    def test_users(self, auth_client, get_or_create_token):
        url = reverse("user-list")
        response = auth_client.get(
            url, format="json", HTTP_AUTHORIZATION="Token " + get_or_create_token.key
        )
        assert response.status_code == 200

    @pytest.mark.usefixtures("auth_client", "get_or_create_token", "create_user")
    def test_user_detail(self, auth_client, get_or_create_token, create_user):
        url = reverse("user-detail", kwargs={"pk": create_user.id})
        response = auth_client.get(
            url,
            format="json",
            HTTP_AUTHORIZATION="Token " + get_or_create_token.key,
        )
        assert response.data.get("email") == create_user.email
        assert response.status_code == 200
