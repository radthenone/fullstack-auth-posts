from datetime import datetime
from uuid import uuid4


def avatar_upload_path(instance: "users.UserBasic | users.UserPremium"):
    now = datetime.now()
    path = f'avatars/{now.strftime("%Y/%m/%d")}/{instance.user.email}/'
    return path


def set_username(email: str):
    try:
        first_part_username = email.split("@")[0]
        uuid_hash = str(uuid4().hex)
        username = f"{first_part_username}_{uuid_hash}"
    except AttributeError:
        username = ""
    return username
