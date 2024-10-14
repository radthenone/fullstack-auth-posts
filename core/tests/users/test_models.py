import pytest


@pytest.mark.django_db
def test_user_friend_requests_factory(user_friend_requests_factory_model):
    assert len(user_friend_requests_factory_model.friend_requests) == 3
