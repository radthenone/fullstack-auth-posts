from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.utils import avatar_upload_path

# Create your models here.


class User(AbstractUser):
    BASIC = "BA"
    PREMIUM = "PM"

    TYPE_ROLES = [(BASIC, _("Basic")), (PREMIUM, _("Premium"))]
    username = models.CharField(
        max_length=150,
        default="",
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )
    roles = models.CharField(
        verbose_name="Roles",
        choices=TYPE_ROLES,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_basic = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        abstract = True


class UserPremium(Profile):
    is_basic = models.BooleanField(default=False, editable=False)
    is_premium = models.BooleanField(default=True, editable=False)


class UserBasic(Profile):
    is_basic = models.BooleanField(default=True, editable=False)
    is_premium = models.BooleanField(default=False, editable=False)
