import uuid
from typing import TYPE_CHECKING, Optional

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from apps.users.types import (
        FriendshipModelType,
        UserModelType,
    )


class CustomFriendshipManager(BaseUserManager):
    def get_object(self, pk: int | uuid.UUID) -> Optional["FriendshipModelType"]:
        try:
            return self.get_queryset().get(id=pk)
        except self.model.DoesNotExist:
            return None

    def add_friend(
        self, from_user: "UserModelType", to_user: "UserModelType"
    ) -> Optional["FriendshipModelType"]:
        from apps.users.models import User

        if to_user not in User.objects.all():
            raise ValueError("User does not exist")
        else:
            return self.get_queryset().create(from_user=from_user, to_user=to_user)

    def remove_friend(
        self, from_user: "UserModelType", to_user: "UserModelType"
    ) -> None:
        from apps.users.models import User

        if to_user not in User.objects.all():
            raise ValueError("User does not exist")
        else:
            friend = self.get_queryset().get(from_user=from_user, to_user=to_user)
            friend.delete()
