from apps.users.models import User, UserBasic, UserPremium
from apps.users.serializers import (
    BasicUserSerializer,
    PremiumUserSerializer,
)
from django.db.models import Model
from django.shortcuts import get_list_or_404, get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response


# TODO separate BasicUserSerializer and PremiumUserSerializer
class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    tag_name = "users"

    def get_queryset(self):
        return get_list_or_404(User.objects.prefetch_related("roles"))

    def get_serializer_class(self, instance=None):
        if isinstance(instance, UserBasic):
            return BasicUserSerializer
        elif isinstance(instance, UserPremium):
            return PremiumUserSerializer

    @extend_schema(
        tags=[tag_name],
        description="List all users",
        request=BasicUserSerializer,
        responses={
            status.HTTP_200_OK: [PremiumUserSerializer, BasicUserSerializer],
        },
    )
    def get(self, request):
        queryset = self.get_queryset()
        data = []
        for user in queryset:
            roles_list = list(user.roles.all().values_list("name", flat=True))
            user_instance = get_object_or_404(
                UserPremium if "PREMIUM" in roles_list else UserBasic, user=user
            )
            serializer_class = self.get_serializer_class(instance=user_instance)
            serializer = serializer_class(user_instance, many=False)
            data.append(serializer.data)
        return Response(data, status=status.HTTP_200_OK)


class UserDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [permissions.IsAuthenticated]
    tag_name = "users"

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

    @extend_schema(
        tags=[tag_name],
        description="Get a user",
        request=[BasicUserSerializer, PremiumUserSerializer],
        responses={
            status.HTTP_200_OK: BasicUserSerializer | PremiumUserSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=[tag_name],
        description="Put a user",
        request=BasicUserSerializer,
        responses={
            status.HTTP_200_OK: BasicUserSerializer | PremiumUserSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=[tag_name],
        description="Patch a user",
        request=BasicUserSerializer,
        responses={
            status.HTTP_200_OK: BasicUserSerializer | PremiumUserSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
        instance.user.delete()

    @extend_schema(
        tags=[tag_name],
        description="Delete a user",
        responses={
            status.HTTP_200_OK: None,
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
