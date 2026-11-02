import base64
from io import BytesIO

import pytest
from apps.auth.utils import encode_token
from django.contrib.auth.hashers import make_password
from PIL import Image
from pytest_factoryboy import register

from tests.users.factories import (
    FriendshipFactory,
    RolesFactory,
    UserBasicFactory,
    UserFactory,
    UserPremiumFactory,
)


@pytest.fixture(scope="function")
def avatar_base64_fixture():
    avatar_image = Image.new("RGB", (200, 200))
    with BytesIO() as buffered:
        avatar_image.save(buffered, format="JPEG")
        avatar_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{avatar_base64}"
    return data_uri


@pytest.fixture
def user_params_fixture():
    return {
        "email": "b@b.com",
        "password": "Test12345!",
    }


@pytest.fixture
def user_register_params_fixture():
    return {
        "email": "register@register.com",
        "password": "Test12345!",
    }


@pytest.fixture
def user_basic_params_fixture(user_params_fixture, avatar_base64_fixture):
    return {
        "user": {
            **user_params_fixture,
        },
        "avatar": avatar_base64_fixture,
        "birth_date": "2000-01-01",
    }


@pytest.fixture
def user_basic_register_params_fixture(
    user_register_params_fixture, avatar_base64_fixture
):
    return {
        "user": {
            **user_register_params_fixture,
        },
        "avatar": avatar_base64_fixture,
        "birth_date": "2000-01-01",
    }


@pytest.fixture(scope="function")
def jwt_token_register_fixture(user_basic_register_params_fixture):
    payload = {
        "email": user_basic_register_params_fixture["user"]["email"],
        "password": make_password(
            user_basic_register_params_fixture["user"]["password"]
        ),
    }
    key = "test"
    return encode_token(payload, key)


# friends
register(
    factory_class=FriendshipFactory,
    _name="friendship_factory_model",
)

# user friends requests
register(
    factory_class=UserFactory,
    friend_requests=3,
    _name="user_friend_requests_factory_model",
)

# user friends added
register(
    factory_class=UserBasicFactory,
    friends=3,
    _name="user_friend_factory_model",
)


# roles
register(
    factory_class=RolesFactory,
    name="BASIC",
    description="Basic role",
    _name="roles_basic_factory_model",
)
register(
    factory_class=RolesFactory,
    name="PREMIUM",
    description="Premium role",
    _name="roles_premium_factory_model",
)

# users
register(
    factory_class=UserFactory,
    _name="user_factory_model",
)
register(
    factory_class=UserBasicFactory,
    roles="BASIC",
    _name="user_basic_factory_model",
)
register(
    factory_class=UserPremiumFactory,
    roles="PREMIUM",
    _name="user_premium_factory_model",
)


@pytest.fixture(scope="function")
def user_factory_model_signup(user_params_fixture):
    user = UserFactory.create(
        email=user_params_fixture["email"],
        password=user_params_fixture["password"],
    )
    return user
