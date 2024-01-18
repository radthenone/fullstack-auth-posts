from datetime import datetime, timedelta
from uuid import uuid4

from django.urls import reverse
import pytest
from django.contrib.auth.hashers import check_password, make_password

pytestmark = pytest.mark.django_db


def test_register_mail_view(mocker, api_client, user_basic_register_params_fixture):
    mocker.patch(
        "apps.emails.tasks.send_register_email",
        return_value=None,
    )
    register_mail_url = reverse("register-mail")
    response = api_client.post(
        register_mail_url,
        data={
            "email": user_basic_register_params_fixture["user"]["email"],
            "password": user_basic_register_params_fixture["user"]["password"],
            "password2": user_basic_register_params_fixture["user"]["password"],
        },
        format="json",
    )
    email = user_basic_register_params_fixture["user"]["email"]
    assert response.data.get("detail") == f"Register email sent to {email}"
    assert response.status_code == 201


def test_register_view(
    mocker,
    api_client,
    jwt_token_register_fixture,
    user_basic_register_params_fixture,
):
    mocker.patch(
        "apps.api.tokens.decode_token",
        return_value={
            "exp": datetime.utcnow() + timedelta(days=14),
            "iat": datetime.utcnow(),
            "jti": uuid4().hex,
            "email": user_basic_register_params_fixture["user"]["email"],
            "password": make_password(
                user_basic_register_params_fixture["user"]["password"]
            ),
        },
    )
    register_url = reverse("register", kwargs={"token": jwt_token_register_fixture})
    response = api_client.post(
        register_url, data=user_basic_register_params_fixture, format="json"
    )

    assert response.status_code == 201


def test_login_view(api_client, user_params_fixture, user_factory_model_signup):
    login_url = reverse("login")
    response = api_client.post(
        login_url,
        data=user_params_fixture,
        format="json",
    )
    logged_in = api_client.login(**user_params_fixture)
    assert logged_in is True
    assert check_password(
        user_params_fixture["password"],
        user_factory_model_signup.password,
    )
    assert response.status_code == 200
