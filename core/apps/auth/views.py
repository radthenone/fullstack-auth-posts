from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions, generics, permissions, status
from rest_framework.response import Response

from apps.api.permissions import UnAuthenticated
from apps.api.tokens import decode_token
from apps.auth.serializers import (
    LoginRefreshSerializer,
    LoginSerializer,
    RegisterMailSerializer,
    RegisterSerializer,
)
from apps.auth.utils import (
    auth_headers_jwt,
    auth_login,
    auth_logout,
    auth_refresh,
)
from apps.emails.tasks import send_refresh_token_email, send_register_email
from apps.emails.utils import CreateMail
from apps.users.models import User
from apps.auth.schema import (
    register_mail_schema,
    register_schema,
    login_schema,
    login_refresh_mail_schema,
    login_refresh_schema,
    logout_schema,
)


class RegisterMailView(generics.GenericAPIView):
    """
    Mail register user
    """

    serializer_class = RegisterMailSerializer
    permission_classes = [permissions.AllowAny]

    @register_mail_schema
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mail = serializer.save()
            send_register_email.delay(**mail)
            return Response(
                data={"detail": f"Register email sent to {serializer.data['email']}"},
                headers={"email_token": mail["message"]["token"]},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    """
    Register user
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @register_schema
    def post(self, request, token):
        data = decode_token(token)
        if "errors" in data:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = request.data.get("user")
        email, password = user.get("email"), user.get("password")

        if check_password(password, data.get("password")) and email == data.get(
            "email"
        ):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                email = serializer.data.get("user").get("email")
                return Response(
                    {"detail": f"User created successfully {email}"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(generics.GenericAPIView):
    """
    Login user
    """

    serializer_class = LoginSerializer
    permission_classes = [UnAuthenticated]

    @login_schema
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                data = auth_login(request=request, **serializer.validated_data)
                return Response(data=data, status=status.HTTP_200_OK)
            except exceptions.AuthenticationFailed as error:
                return Response(
                    {"errors": error.detail},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRefreshMailView(generics.GenericAPIView):
    """
    Login user refresh mail
    """

    serializer_class = LoginRefreshSerializer
    permission_classes = [UnAuthenticated]

    @login_refresh_mail_schema
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
                data={"detail": "Login refresh email sent"},
                headers={"login_token": str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRefreshView(generics.GenericAPIView):
    permission_classes = [UnAuthenticated]
    """
    Login user refresh
    """

    @classmethod
    @login_refresh_schema
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


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @classmethod
    @logout_schema
    def get(cls, request):
        message = auth_logout(request)
        return Response(message, status=status.HTTP_200_OK)
