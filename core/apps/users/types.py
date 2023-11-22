from typing import TypeVar

from apps.users.models import (
    Profile,
    Roles,
    User,
    UserBasic,
    UserPremium,
)
from django.db.models.query import QuerySet

# Roles Types
RolesModelType = TypeVar(
    "RolesModelType",
    bound=Roles,
)
RolesQueryType = TypeVar(
    "RolesQueryType",
    bound=QuerySet[Roles],
)

# User Types
UserModelType = TypeVar(
    "UserModelType",
    bound=User,
)
UserQueryType = TypeVar(
    "UserQueryType",
    bound=QuerySet[User],
)

# User Basic Types
UserBasicModelType = TypeVar(
    "UserBasicModelType",
    bound=UserBasic,
)
UserBasicQueryType = TypeVar(
    "UserBasicQueryType",
    bound=QuerySet[UserBasic],
)

# User Premium Types
UserPremiumModelType = TypeVar(
    "UserPremiumModelType",
    bound=UserPremium,
)
UserPremiumQueryType = TypeVar(
    "UserPremiumQueryType",
    bound=QuerySet[UserPremium],
)

# User Profile Types
ProfileModelType = TypeVar(
    "ProfileModelType",
    bound=Profile,
)
ProfileQueryType = TypeVar(
    "ProfileQueryType",
    bound=QuerySet[Profile],
)
