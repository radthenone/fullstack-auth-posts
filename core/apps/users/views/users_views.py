from typing import Any
from apps.users.models import User, UserBasic, UserPremium
from apps.users.serializers import (
    UserSerializer,
    BasicUserSerializer,
    PremiumUserSerializer,
)
from rest_framework import generics, permissions, mixins, status
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import QuerySet, Model
from apps.users.types import UserPremiumQueryType, UserBasicQueryType
from django.shortcuts import get_object_or_404, get_list_or_404


class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return get_list_or_404(User.objects.get_related_roles())

    def get_serializer_class(self, instance=None):
        if isinstance(instance, UserBasic):
            return BasicUserSerializer
        elif isinstance(instance, UserPremium):
            return PremiumUserSerializer

    def get(self, request):  # noqa
        qs = self.get_queryset()
        data = []
        for user in qs:
            roles_list = list(user.roles.all().values_list("name", flat=True))
            if "PREMIUM" in roles_list:
                instance = get_object_or_404(UserPremium, user=user)
                serializer_class = self.get_serializer_class(instance=instance)
            else:
                instance = get_object_or_404(UserBasic, user=user)
                serializer_class = self.get_serializer_class(instance=instance)
            serializer = serializer_class(instance, many=False)
            data.append(serializer.data)
        return Response(data, status=status.HTTP_200_OK)


class UserDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Model | None:
        user = self.request.user
        if UserBasic.objects.filter(user=user).exists():
            return get_object_or_404(UserBasic, user=user)
        elif UserPremium.objects.filter(user=user).exists():
            return get_object_or_404(UserPremium, user=user)

    def get_serializer_class(self):
        instance = self.get_object()
        if isinstance(instance, UserBasic):
            return BasicUserSerializer
        elif isinstance(instance, UserPremium):
            return PremiumUserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
        instance.user.delete()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
