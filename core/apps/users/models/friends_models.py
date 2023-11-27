from apps.users.models.abstract_models import CreatedUpdatedMixin
from django.db import models
from django.conf import settings
from apps.users.managers import CustomFriendshipManager


class Friendship(CreatedUpdatedMixin):
    from_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="from_user",
    )
    to_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="to_user",
    )
    is_accepted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    objects = CustomFriendshipManager()

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"
