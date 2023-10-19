from datetime import datetime
from uuid import uuid4
from PIL import Image, ImageOps
import base64
from django.db.models.fields.files import FieldFile
import os
from io import BytesIO


def avatar_upload_path(instance: "users.UserBasic | users.UserPremium") -> str:
    now = datetime.now()
    path = f'avatars/{now.strftime("%Y/%m/%d")}/{instance.user.email}/'
    return path


def avatar_format(file: FieldFile) -> str:
    return file.path.split(".")[-1]


def avatar_thumbnail_size(file: FieldFile, width: int, height: int):
    size = (width, height)
    image_name = os.path.basename(file.path)
    with Image.open(file) as image:
        image = ImageOps.contain(image=image, size=size)
        image.thumbnail(size)
        image.save(image_name)
    return image


def avatar_render_to_base64(file: FieldFile) -> str:
    to_format = avatar_format(file).upper()
    with Image.open(file) as image:
        buffer = BytesIO()
        image.save(buffer, format=to_format)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def set_username(email: str) -> str | None:
    try:
        first_part_username = email.split("@")[0]
        uuid_hash = uuid4().hex
        username = f"{first_part_username}_{uuid_hash}"
        return username
    except AttributeError:
        return None
