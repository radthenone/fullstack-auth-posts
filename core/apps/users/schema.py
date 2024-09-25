from drf_spectacular.utils import (
    extend_schema,
)
from apps.users.serializers import (
    BasicUserSerializer,
    PremiumUserSerializer,
)
from rest_framework import status

users_schema = extend_schema(
    tags=["users"],
    description="List all users",
    request=BasicUserSerializer,
    responses={
        status.HTTP_200_OK: [PremiumUserSerializer, BasicUserSerializer],
    },
)
