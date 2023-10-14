from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.types import UserModelType, UserQueryType


class RolesQuerySet(models.QuerySet):
    def get_by_name(self, name):
        return self.get(name=name)


class UserQuerySet(models.QuerySet):
    def get_by_email(self, email) -> "UserModelType":
        return self.get(email=email)
