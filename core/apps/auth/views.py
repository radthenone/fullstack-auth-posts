from apps.api.tokens import decode_token
from apps.auth.serializers import (
    LoginSerializer,
    RegisterMailSerializer,
    RegisterSerializer,
    LoginRefreshSerializer,
    RegisterUserSerializer,
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
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiTypes,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiRequest,
    OpenApiExample,
)
from config.schemas import get_schema


class RegisterMailView(generics.GenericAPIView):
    serializer_class = RegisterMailSerializer
    tag_name = "auth"
    open_api_example = get_schema("register_mail_view")

    @extend_schema(
        tags=[tag_name],
        description="Register user mail",
        examples=[
            OpenApiExample(name=str(n), value=item)
            for n, item in enumerate(open_api_example)
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response={
                    "detail": "Register email sent",
                },
                description="Register email sent",
                examples=[
                    OpenApiExample(
                        name=str(n),
                        value={
                            "detail": f"Register email sent to {item['email']}",
                        },
                    )
                    for n, item in enumerate(open_api_example)
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"detail": "Invalid credentials"},
                description="Invalid credentials",
                examples=[
                    OpenApiExample(name=str(n), value={"detail": "Invalid credentials"})
                    for n, item in enumerate(open_api_example)
                ],
            ),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mail = serializer.save()
            send_register_email.delay(**mail)
            return Response(
                data={"detail": "Register email sent"},
                headers={"email_token": mail["message"]["token"]},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    tag_name = "auth"
    open_api_example = get_schema("register_view")

    @extend_schema(
        tags=[tag_name],
        description="Register user",
        examples=[
            OpenApiExample(name=str(n), value=item)
            for n, item in enumerate(open_api_example)
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response={"detail": "User created successfully"},
                description="User created",
                examples=[
                    OpenApiExample(
                        name=str(n),
                        value={
                            "detail": f"User {item['user']['email']} created successfully"
                        },
                    )
                    for n, item in enumerate(open_api_example)
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"detail": "Invalid credentials"},
                description="Invalid credentials",
                examples=[
                    OpenApiExample(name=str(n), value={"detail": "Invalid credentials"})
                    for n, item in enumerate(open_api_example)
                ],
            ),
        },
    )
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
    serializer_class = LoginSerializer
    tag_name = "auth"
    open_api_example = get_schema("login_view")

    @extend_schema(
        tags=[tag_name],
        description="Login user",
        examples=[
            OpenApiExample(
                name=str(n),
                value=item,
            )
            for n, item in enumerate(open_api_example)
        ],
        request=LoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={"access": "Token", "refresh": "Token"},
                description="Login user",
                examples=[
                    OpenApiExample(
                        name=str(n),
                        value={
                            "access": "Token",
                            "refresh": "Token",
                        },
                    )
                    for n, _ in enumerate(open_api_example)
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={"detail": "Token is invalid or expired"},
                description="Invalid credentials",
                examples=[
                    OpenApiExample(
                        name=str(n),
                        value={
                            "detail": "Token is invalid or expired",
                        },
                    )
                    for n, _ in enumerate(open_api_example)
                ],
            ),
        },
    )
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
    tag_name = "auth"

    @extend_schema(
        tags=[tag_name],
        description="Login user refresh mail",
        request=LoginRefreshSerializer,
        responses={
            status.HTTP_200_OK: LoginRefreshSerializer,
        },
    )
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
    tag_name = "auth"

    @classmethod
    @extend_schema(
        tags=[tag_name],
        description="Login user refresh",
        request={
            "type": "object",
            "properties": {
                "token": {"type": "string"},
            },
            "required": ["token"],
        },
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                },
            },
            status.HTTP_400_BAD_REQUEST: {
                "type": "string",
                "example": "Invalid token",
            },
        },
    )
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
    tag_name = "auth"

    @classmethod
    @extend_schema(
        tags=[tag_name],
        description="Logout",
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
                "description": "Successfully logged out",
            },
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
                "description": "Invalid user",
            },
        },
    )
    def get(cls, request):
        message = auth_logout(request)
        return Response(message, status=status.HTTP_200_OK)
