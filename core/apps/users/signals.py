from typing import TYPE_CHECKING

from apps.users.models import Profile
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

if TYPE_CHECKING:
    from apps.users.types import ProfileModelType, UserModelType


@receiver(signal=pre_save, sender=settings.AUTH_USER_MODEL)
def create_username(
    sender: "UserModelType",
    instance: "UserModelType",
    **kwargs: dict,
) -> None:
    from apps.users.utils import set_username

    if not instance.username:
        instance.username = set_username(instance.email)


@receiver(signal=post_save, sender=Profile)
def create_avatar_base64(
    sender: "ProfileModelType",
    instance: "ProfileModelType",
    created: bool,
    **kwargs: dict,
) -> None:
    from apps.users.utils import avatar_render_to_base64

    instance.avatar = avatar_render_to_base64(instance.avatar)


@receiver(signal=pre_save, sender=Profile)
def create_avatar_thumbnail(
    sender: "ProfileModelType",
    instance: "ProfileModelType",
    **kwargs: dict,
) -> None:
    from apps.users.utils import avatar_thumbnail_size

    instance.avatar = avatar_thumbnail_size(
        instance.avatar,
        100,
        100,
    )
