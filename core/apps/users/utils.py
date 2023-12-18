from datetime import datetime
from typing import TYPE_CHECKING, Union
from uuid import uuid4

if TYPE_CHECKING:
    from apps.users.types import UserBasicModelType, UserPremiumModelType


def avatar_upload_path(
    instance: Union["UserBasicModelType", "UserPremiumModelType"], filename: str
) -> str:
    now = datetime.now()
    return f'avatars/{instance.user.email}/{now.strftime("%Y/%m/%d")}/{filename}'


def set_username(email: str) -> str | None:
    try:
        first_part_username = email.split("@")[0]
        uuid_hash = uuid4().hex
        username = f"{first_part_username}_{uuid_hash}"
        return username
    except AttributeError:
        return None
