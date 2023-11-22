from apps.users.models.abstract import CreatedUpdatedMixin
from django.db import models
from django.conf import settings


class Friendship(models.Model, CreatedUpdatedMixin):
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
    accepted = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"
