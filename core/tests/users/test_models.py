from apps.users.models import (
    User,
    UserBasic,
    UserPremium,
    Roles,
    Friendship,
)
from tests.users.factories import (
    UserFactory,
    UserBasicFactory,
    UserPremiumFactory,
    RolesFactory,
    FriendshipFactory,
)
import pytest
from apps.api.tokens import encode_token


@pytest.mark.django_db
def test_user_friend_requests_factory(user_friend_requests_factory_model):
    assert len(user_friend_requests_factory_model.friend_requests) == 3
