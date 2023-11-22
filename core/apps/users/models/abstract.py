from django.conf import settings
from apps.users.utils import avatar_format, avatar_upload_path
from django.core import exceptions
from django.db import models
from django.db.models.fields.files import FieldFile
from PIL import Image
from typing import Callable
from datetime import datetime
from functools import wraps


# Create your models here.
class Validators:
    @staticmethod
    def validate_birth_date(date: datetime) -> None:
        years = datetime.now().year - date.year
        if years < 18:
            raise exceptions.ValidationError("You must be at least 18 years old")

    @classmethod
    def validate_image_size(
        cls, width: int, height: int
    ) -> Callable[[FieldFile], None]:
        @wraps(wrapped=cls.validate_image_size)
        def validator(file: FieldFile) -> None:
            image = Image.open(file.path)
            if (width is not None and image.width < width) or (
                height is not None and image.height < height
            ):
                raise exceptions.ValidationError(
                    f"Size should be at least {width} x {height} pixels."
                )

        return validator

    @classmethod
    def validate_image_format(
        cls, allowed_formats: list
    ) -> Callable[[FieldFile], None]:
        @wraps(wrapped=cls.validate_image_format)
        def validator(file: FieldFile) -> None:
            to_format = avatar_format(file).lower()
            if to_format not in allowed_formats:
                raise exceptions.ValidationError(
                    f'Wrong image format, expected: {", ".join(allowed_formats)}.'
                )

        return validator


class CreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProfileMixin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True,
        validators=[
            Validators.validate_image_size(width=200, height=200),
            Validators.validate_image_format(allowed_formats=["png", "jpeg", "jpg"]),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(
        verbose_name="Birth Date",
        null=True,
        blank=True,
        validators=[Validators.validate_birth_date],
    )
    is_premium = models.BooleanField(default=False)
    is_basic = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.email

    @property
    def age(self):
        return datetime.now().year - self.birth_date.year if self.birth_date else 0

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
