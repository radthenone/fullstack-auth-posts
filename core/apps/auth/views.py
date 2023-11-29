import json

from apps.api.tokens import decode_token
from apps.auth.serializers import (
    LoginSerializer,
    RegisterMailSerializer,
    RegisterSerializer,
    LoginRefreshSerializer,
)
from apps.auth.utils import (
    auth_headers_jwt,
    auth_login,
    auth_logout,
    auth_refresh,
)
from apps.emails.tasks import send_register_email, send_refresh_token_email
from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.response import Response
from apps.emails.utils import CreateMail
from django.conf import settings
from apps.users.models import User


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
        data = decode_token(token)
        if "errors" in data:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        email, password = request.data.get("email"), request.data.get("password")

        if check_password(password, data.get("password")) and email == data.get(
            "email"
        ):
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


class LoginRefreshMailView(generics.GenericAPIView):
    serializer_class = LoginRefreshSerializer

    def post(self, request):
        email = request.data.get("email")
        serializer = self.serializer_class(data={"email": email})
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data.get("token")
            exp_minutes = serializer.validated_data.get("exp_minutes")
            mail = CreateMail(
                send_email=email,
                title="Login refresh",
                extra_message={
                    "refresh_url": f"{settings.DOMAIN_URL}/api/auth/login/refresh/{token}/",
                },
                info=f"Kindly use this token to re-login. \
                Only valid for {exp_minutes} minutes.",
            )
            send_refresh_token_email.delay(**mail)
            return Response(
                {"detail": "Login refresh email sent"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRefreshView(generics.GenericAPIView):
    @classmethod
    def get(cls, request, token):
        if token:
            data = decode_token(token)
            if "errors" in data:
                return Response(
                    {"errors": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = User.objects.get(email=data["email"])
                if user:
                    refresh_data = auth_refresh(user)
                    return Response(refresh_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


# TODO : add serializer
class LogoutView(generics.GenericAPIView):
    @classmethod
    def get(cls, request):
        message = auth_logout(request)
        return Response({"detail": message}, status=status.HTTP_200_OK)
