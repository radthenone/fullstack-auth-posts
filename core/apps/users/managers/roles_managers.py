from typing import TYPE_CHECKING, Optional

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from apps.users.types import (
        RolesModelType,
        UserModelType,
    )


class CustomRolesManager(BaseUserManager):
    def get_role(self, name: str) -> Optional["RolesModelType"]:
        try:
            return self.get(name=name)
        except RolesModelType.DoesNotExist:
            return None

    def create_role(self, name: str) -> "RolesModelType":
        return self.get_queryset().create(name=name)

    def get_object_by_name(self, name: str) -> Optional["RolesModelType"]:
        return self.get_queryset().get_role(name=name)

    def get_admin_queryset(self) -> Optional["RolesModelType"]:
        return self.get_queryset().get_role(name="ADMIN")

    def get_basic_queryset(self) -> Optional["RolesModelType"]:
        return self.get_queryset().get_role(name="BASIC")

    def get_premium_queryset(self) -> Optional["RolesModelType"]:
        return self.get_queryset().get_role(name="PREMIUM")

    def get_list_with_names(self, *args, flat=True) -> list:
        return self.get_queryset().values_list(*args, flat=flat)

    def set_role(
        self, role: Optional[str], user: "UserModelType", **extra_fields
    ) -> None:
        from apps.users.models import UserBasic, UserPremium

        if role in list(self.get_queryset().objects.values_list("name", flat=True)):
            if role == "ADMIN":
                user.roles.set([self.get_admin_queryset()])
            elif role == "BASIC" or role is None:
                user.roles.set([self.get_basic_queryset()])
                UserBasic.objects.create(user=user, **extra_fields)
            elif role == "PREMIUM":
                user.roles.set([self.get_premium_queryset()])
                UserPremium.objects.create(user=user, **extra_fields)
            else:
                user.roles.set([self.get_role(name=role)])
        else:
            raise ValueError(f"Role {role} does not exist")
