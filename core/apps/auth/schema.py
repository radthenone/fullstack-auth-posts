from config.schemas import get_schema
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from apps.auth.serializers import (
    LoginRefreshSerializer,
    LoginSerializer,
    RegisterMailSerializer,
    RegisterSerializer,
)
from rest_framework import status

templates = {
    "register_mail_view": get_schema("auth").get("register_mail_view"),
    "register_user_view": get_schema("auth").get("register_user_view"),
    "login_view": get_schema("auth").get("login_view"),
    "login_refresh_mail_view": get_schema("auth").get("login_refresh_mail_view"),
}

register_mail_schema = extend_schema(
    tags=["auth"],
    description="""
        Mail register user \n
        Panel to send first register data with mail, then gets token to verify register panel in next registry step.
        """,
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": templates["register_mail_view"]["value"]["email"],
                },
                "password": {
                    "type": "string",
                    "example": templates["register_mail_view"]["value"]["password"],
                },
                "password2": {
                    "type": "string",
                    "example": templates["register_mail_view"]["value"]["password2"],
                },
            },
        }
    },
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response={
                "example": {
                    "detail": f"Register email sent to {templates['register_mail_view']['value']['email']}",
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "example": {
                    "errors": "Invalid credentials",
                }
            }
        ),
    },
)

register_schema = extend_schema(
    tags=["auth"],
    description="""
        Register user \n
        Basic user panel creator.
        """,
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "example": templates["register_user_view"]["value"]["user"],
                },
                "avatar": {
                    "type": "string",
                    "example": templates["register_user_view"]["value"]["avatar"],
                },
                "birth_date": {
                    "type": "string",
                    "example": templates["register_user_view"]["value"]["birth_date"],
                },
            },
        }
    },
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response={
                "example": {
                    "detail": f"User created successfully {templates['register_user_view']['value']['user']['email']}",
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "example": {
                    "errors": "Invalid credentials",
                }
            }
        ),
    },
)

login_schema = extend_schema(
    tags=["auth"],
    description="Login user",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": templates["login_view"]["value"]["email"],
                },
                "password": {
                    "type": "string",
                    "example": templates["login_view"]["value"]["password"],
                },
            },
        }
    },
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={
                "properties": {
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                }
            },
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response={
                "example": {
                    "errors": "Token is invalid or expired",
                }
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "example": {
                    "errors": "Invalid credentials",
                }
            }
        ),
    },
)

login_refresh_mail_schema = extend_schema(
    tags=["auth"],
    description="Login user refresh mail",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": templates["login_refresh_mail_view"]["value"]["email"],
                }
            },
        }
    },
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response={
                "example": {
                    "detail": "Login refresh email sent",
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "example": {
                    "errors": "Invalid credentials",
                }
            }
        ),
    },
)

login_refresh_schema = extend_schema(
    tags=["auth"],
    description="""
        Refresh login user \n
        Send token from email response
        """,
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
                "access": {"type": "string"},
                "refresh": {"type": "string"},
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "type": "string",
            "example": {"errors": "Invalid token"},
        },
    },
)

logout_schema = extend_schema(
    tags=["auth"],
    description="Logout",
    responses={
        status.HTTP_200_OK: {
            "type": "object",
            "properties": {
                "detail": {
                    "type": "string",
                    "example": "Successfully logged out",
                },
            },
        }
    },
)
