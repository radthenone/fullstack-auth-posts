import uuid
from apps.users.managers import CustomUserManager, CustomRolesManager
from apps.users.utils import avatar_upload_path
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import exceptions, validators
from datetime import datetime
from apps.users.utils import set_username


# Create your models here.
class Validators:
    validate_email_style = validators.RegexValidator(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|pl)$",
        message="Enter a valid email address with either .com or .pl domain.",
        code="invalid_email",
    )

    @staticmethod
    def validate_birth_date(date: datetime):
        years = datetime.now().year - date.year
        if years < 18:
            raise exceptions.ValidationError("You must be at least 18 years old")


class Roles(models.Model):
    name = models.CharField(max_length=20, default="BASIC")
    description = models.TextField(default="")
    objects = CustomRolesManager()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"


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
    roles = models.ManyToManyField(to=Roles, related_name="users", blank=False)
    friends = models.ManyToManyField(
        to="self",
        blank=True,
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
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return ""

    def save(self, *args, **kwargs):
        self.full_clean()
        self.username = set_username(self.email)
        if self.change_password:
            self.set_password(self.password)
            self.change_password = False
        return super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
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
        if self.birth_date is None:
            return 0
        today_year = datetime.now().year
        birth_year = self.birth_date.year
        age = today_year - birth_year
        return age

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class UserPremium(Profile):
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


class UserBasic(Profile):
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
