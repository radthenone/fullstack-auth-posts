import uuid
from typing import TYPE_CHECKING, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

if TYPE_CHECKING:
    from apps.users.types import (
        UserModelType,
    )


class CustomUserManager(BaseUserManager):
    def get_user(self, user_id: int | uuid.UUID) -> Optional["UserModelType"]:
        try:
            return self.get_queryset().get(id=user_id)
        except self.model.DoesNotExist:
            return None

    def delete_user(self, user_id: int | uuid.UUID) -> None:
        user = self.get_user(user_id=user_id)
        user.delete()

    def update_user(
        self, user_id: int | uuid.UUID, **kwargs
    ) -> Optional["UserModelType"]:
        user = self.get_user(user_id=user_id)
        user.update(**kwargs)
        return user

    @transaction.atomic
    def create_user(
        self, email: str, password: str, roles: str = None, **extra_fields
    ) -> "UserModelType":
        from apps.users.models import Roles, UserBasic, UserPremium

        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        if not password:
            raise ValueError("The Password must be set")
        validate_password(password)
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            change_password=True,
            password=password,
            **extra_fields,
        )
        user.save()

        if roles == "PREMIUM":
            user.roles.set([Roles.objects.get_premium_queryset()])
            UserPremium.objects.create(user=user)
        else:
            user.roles.set([Roles.objects.get_basic_queryset()])
            UserBasic.objects.create(user=user)
        return user

    @transaction.atomic
    def create_superuser(
        self, email: str, password: str, roles=None, **extra_fields
    ) -> "UserModelType":
        from apps.users.models import Roles, UserPremium

        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            change_password=True,
            password=password,
            **extra_fields,
        )
        user.save()
        if not user.roles.exists():
            user.roles.set(
                [
                    Roles.objects.get_admin_queryset(),
                    Roles.objects.get_premium_queryset(),
                ]
            )
            UserPremium.objects.create(user=user)
        else:
            if roles in ["ADMIN"]:
                user.roles.set(roles)
        return user
