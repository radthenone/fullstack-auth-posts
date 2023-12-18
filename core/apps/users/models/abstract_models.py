from django.conf import settings
from apps.users.utils import avatar_upload_path
from django.core import exceptions
from django.db import models
from datetime import datetime


# Create your models here.
class Validators:
    @staticmethod
    def validate_birth_date(date: datetime) -> None:
        years = datetime.now().year - date.year
        if years < 18:
            raise exceptions.ValidationError("You must be at least 18 years old")


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
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True,
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
