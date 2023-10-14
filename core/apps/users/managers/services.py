from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from apps.users.managers.repository import RolesQuerySet, UserQuerySet
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from apps.users.types import UserModelType, UserQueryType


class CustomRolesManager(BaseUserManager):
    def get_queryset(self) -> RolesQuerySet:
        return RolesQuerySet(self.model, using=self._db)

    def get_object_by_name(self, name):
        return self.get_queryset().get_by_name(name=name)

    def get_admin_queryset(self):
        return self.get_queryset().get_by_name(name="ADMIN")

    def get_basic_queryset(self):
        return self.get_queryset().get_by_name(name="BASIC")

    def get_premium_queryset(self):
        return self.get_queryset().get_by_name(name="PREMIUM")

    def get_list_with_names(self, *args, flat=True):
        return self.get_queryset().values_list(*args, flat=flat)

    def set_role(self, role, user, **extra_fields):
        from apps.users.models import UserBasic, UserPremium

        if role == "ADMIN":
            user.roles.set([self.get_admin_queryset()])
        elif role == "BASIC" or role is None:
            user.roles.set([self.get_basic_queryset()])
            UserBasic.objects.create(user=user, **extra_fields)
        elif role == "PREMIUM":
            user.roles.set([self.get_premium_queryset()])
            UserPremium.objects.create(user=user, **extra_fields)


class CustomUserManager(BaseUserManager):
    def get_queryset(self) -> "UserQueryType":
        return UserQuerySet(self.model, using=self._db)

    def get_related_friends(self):
        return self.prefetch_related("friends").all()

    def get_related_roles(self):
        return self.prefetch_related("roles").all()

    def get_object_by_email(self, email) -> Union["UserModelType", None]:
        try:
            return self.get_queryset().get_by_email(email=email)
        except self.model.DoesNotExist:
            return None

    def get_users_roles_names(self):
        return [
            list(user.roles.all().values_list("name", flat=True))
            for user in self.get_related_roles()
        ]

    def create_user(self, email: str, password: str, roles=None, **extra_fields):
        from apps.users.models import Roles, UserBasic

        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        if password:
            validate_password(password)
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            change_password=True,
            password=password,
            **extra_fields,
        )
        user.save()
        if not user.roles.exists() and not roles:
            UserBasic.objects.create(user=user)
        else:
            if roles in list(Roles.objects.values_list("name", flat=True)):
                Roles.objects.set_role(role=roles, user=user)
        return user

    def create_superuser(self, email: str, password: str, roles=None, **extra_fields):
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
