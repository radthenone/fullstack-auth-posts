import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from apps.users.managers import CustomUserManager
from apps.users.models.abstract_models import ProfileMixin
from apps.users.models.friends_models import Friendship
from apps.users.models.roles_models import Roles
from apps.users.utils import set_username


# Create your models here.
class Validators:
    validate_email_style = validators.RegexValidator(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|pl)$",
        message="Enter a valid email address with either .com or .pl domain.",
        code="invalid_email",
    )


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(
        blank=True,
        max_length=150,
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        blank=False,
        validators=[Validators.validate_email_style],
    )
    roles = models.ManyToManyField(to=Roles, related_name="roles", blank=False)
    friends = models.ManyToManyField(
        to="self",
        blank=True,
        through=Friendship,
        through_fields=("from_user", "to_user"),
        symmetrical=True,
    )
    friend_requests = models.JSONField(default=dict, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    # extra flags
    is_locked = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    change_password = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["-date_joined"]),
        ]
        verbose_name = "user"
        verbose_name_plural = "users"
        constraints = (
            models.UniqueConstraint(
                fields=["email", "username"],
                name="unique_user",
            ),
        )

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else ""
        )

    @staticmethod
    def get_friends_response_url(token: str) -> str:
        return f"{settings.DOMAIN_URL}/api/users/friend/response/{token}"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.username = set_username(self.email)
        if self.change_password:
            self.set_password(self.password)
            self.change_password = False
        return super().save(*args, **kwargs)


class UserPremium(ProfileMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="premium_profile",
    )
    is_basic = models.BooleanField(default=False, editable=False)
    is_premium = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name = "premium user"
        verbose_name_plural = "premium users"

    def __str__(self):
        return self.user.email


class UserBasic(ProfileMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="basic_profile",
    )
    is_basic = models.BooleanField(default=True, editable=False)
    is_premium = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "basic user"
        verbose_name_plural = "basic users"

    def __str__(self):
        return self.user.email
