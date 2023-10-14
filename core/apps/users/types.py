from typing import TypeVar
from django.db.models.query import QuerySet
from apps.users.managers import (
    CustomUserManager,
    CustomRolesManager,
)
from apps.users.models import (
    Roles,
    User,
    UserBasic,
    UserPremium,
)
from apps.users.serializers import (
    RolesSerializer,
    UserSerializer,
    BasicUserSerializer,
    PremiumUserSerializer,
)

RolesManagerType = TypeVar(
    "RolesManagerType",
    bound=CustomRolesManager,
)

RolesModelType = TypeVar(
    "RolesModelType",
    bound=Roles,
)

RolesQuerySet = TypeVar(
    "RolesQuerySet",
    bound=QuerySet[Roles],
)
RolesSerializerType = TypeVar(
    "RolesSerializerType",
    bound=RolesSerializer,
)

UserModelType = TypeVar(
    "UserModelType",
    bound=User,
)
UserQueryType = TypeVar(
    "UserQueryType",
    bound=QuerySet[User],
)
UserSerializerType = TypeVar(
    "UserSerializerType",
    bound=UserSerializer,
)

UserBasicModelType = TypeVar(
    "UserBasicModelType",
    bound=UserBasic,
)
UserBasicQueryType = TypeVar(
    "UserBasicQueryType",
    bound=QuerySet[UserBasic],
)
BasicUserSerializerType = TypeVar(
    "BasicUserSerializerType",
    bound=BasicUserSerializer,
)

UserPremiumModelType = TypeVar(
    "UserPremiumModelType",
    bound=UserPremium,
)
UserPremiumQueryType = TypeVar(
    "UserPremiumQueryType",
    bound=QuerySet[UserPremium],
)
PremiumUserSerializerType = TypeVar(
    "PremiumUserSerializerType",
    bound=PremiumUserSerializer,
)
