from apps.users.managers import CustomUserManager
from apps.users.utils import avatar_upload_path
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    BASIC = "BA"
    PREMIUM = "PM"

    TYPE_ROLES = [(BASIC, _("Basic")), (PREMIUM, _("Premium"))]
    username = models.CharField(
        blank=True,
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
        default=BASIC,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return ""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_basic = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.email


class UserPremium(Profile):
    is_basic = models.BooleanField(default=False, editable=False)
    is_premium = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name = _("premium user")
        verbose_name_plural = _("premium users")

    def __str__(self):
        return self.user.email


class UserBasic(Profile):
    is_basic = models.BooleanField(default=True, editable=False)
    is_premium = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = _("basic user")
        verbose_name_plural = _("basic users")

    def __str__(self):
        return self.user.email
