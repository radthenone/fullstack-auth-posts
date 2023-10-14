from apps.users.serializers import RolesSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response
from rest_framework import status, permissions
from apps.users.models import Roles
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django.shortcuts import get_object_or_404


class RolesListView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        queryset = Roles.objects.all()
        name = kwargs.get("name", None)
        if name is not None:
            queryset = Roles.objects.filter(name=name)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            )
        ],
    )
    def get(self, request):
        name = request.query_params.get("name")
        self.queryset = self.get_queryset(name=name)
        serializer = RolesSerializer(
            instance=self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class RolesDetailView(GenericAPIView):
    serializer_class = RolesSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "name"
    queryset = Roles.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.queryset, name=self.kwargs.get(self.lookup_field, None)
        )
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        name = kwargs.get("name", None)
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": f"Role {name} has been deleted"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
