from typing import TYPE_CHECKING, Optional

from django.db import models

if TYPE_CHECKING:
    from apps.users.types import RolesModelType, UserModelType


class RolesQuerySet(models.QuerySet):
    def get_by_name(self, name: str) -> Optional["RolesModelType"]:
        try:
            return self.get(name=name)
        except RolesModelType.DoesNotExist:
            return None


class UserQuerySet(models.QuerySet):
    def get_by_email(self, email: str) -> Optional["UserModelType"]:
        try:
            return self.get(email=email)
        except UserModelType.DoesNotExist:
            return None
