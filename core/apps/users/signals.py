from typing import TYPE_CHECKING

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

if TYPE_CHECKING:
    from apps.users.types import UserModelType


@receiver(signal=pre_save, sender=settings.AUTH_USER_MODEL)
def create_username(
    sender: "UserModelType",
    instance: "UserModelType",
    **kwargs: dict,
) -> None:
    from apps.users.utils import set_username

    if not instance.username:
        instance.username = set_username(instance.email)
