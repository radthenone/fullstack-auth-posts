from typing import TYPE_CHECKING, Optional

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from apps.users.types import (
        RolesModelType,
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
        return self.get_role(name=name)

    def get_admin_queryset(self) -> Optional["RolesModelType"]:
        return self.get_role(name="ADMIN")

    def get_basic_queryset(self) -> Optional["RolesModelType"]:
        return self.get_role(name="BASIC")

    def get_premium_queryset(self) -> Optional["RolesModelType"]:
        return self.get_role(name="PREMIUM")

    def get_list_with_names(self, *args, flat=True) -> list:
        return self.get_queryset().values_list(*args, flat=flat)
