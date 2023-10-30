from rest_framework.response import Response
from rest_framework import generics, status, parsers
from apps.auth.serializers import (
    RegisterMailSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from apps.api.tokens import decode_token
from django.contrib.auth.hashers import check_password
from apps.emails.tasks import send_register_email
from apps.auth.utils import (
    auth_login,
    auth_logout,
    auth_refresh,
    auth_headers_jwt,
)
import json


class RegisterMailView(generics.GenericAPIView):
    serializer_class = RegisterMailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mail = serializer.save()
            send_register_email.delay(**mail)
            return Response(
                data={"detail": "Register email sent"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, token):
        user = request.data.get("user")
        if isinstance(user, str):
            user = json.loads(user)
            request.data["user"] = user
        data = decode_token(token)
        if "errors" in data:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        email, password = user.get("email"), user.get("password")

        if check_password(password, data.get("password")) and email == data.get(
            "email"
        ):
            request.data["user"]["password"] = data.get("password")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                email = instance.data.get("email")
                return Response(
                    {"detail": f"User created successfully {email}"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            {"errors": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                data = auth_login(request=request, **serializer.validated_data)
                headers = auth_headers_jwt(data["access_token"])
                return Response(data=data, headers=headers, status=status.HTTP_200_OK)
            except ValueError as error:
                return Response(
                    {"errors": str(error)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRefreshView(generics.GenericAPIView):
    @classmethod
    def get(cls, request):
        try:
            data = auth_refresh(request)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as error:
            return Response({"errors": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    @classmethod
    def get(cls, request):
        message = auth_logout(request)
        return Response({"detail": message}, status=status.HTTP_200_OK)
