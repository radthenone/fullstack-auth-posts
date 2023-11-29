from apps.api.tokens import encode_token
from apps.users.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from config.redis import cache
from typing import Optional
from rest_framework import exceptions
from django.conf import settings
import datetime


def access_token(user: Optional[User] = None) -> str:
    if not user:
        raise exceptions.AuthenticationFailed("Invalid credentials")
    payload = {
        "token_type": "access",
        "user_id": str(user.id),
        "user_email": user.email,
    }
    return encode_token(payload=payload, exp_minutes=10)


def refresh_token(user: Optional[User] = None) -> None:
    if not user:
        raise exceptions.AuthenticationFailed("Invalid credentials")
    payload = {
        "token_type": "refresh",
        "user_id": str(user.id),
        "user_email": user.email,
    }
    cache.set(
        name=f"refresh_token_{user.id}",
        value=encode_token(
            payload=payload,
            exp_days=14,
            key=settings.SIMPLE_JWT["REFRESH_KEY"],
        ),
        ex=datetime.timedelta(days=14),
    )


def auth_login(request: HttpRequest, email: str, password: str) -> dict[str, str]:
    user = authenticate(email=email, password=password)
    if isinstance(user, User):
        login(request, user)
        refresh_token(user=user)
        return {
            "access_token": access_token(user=user),
            "refresh_token": str(
                cache.get(name=f"refresh_token_{user.id}").decode("utf-8")
            ),
        }
    raise exceptions.AuthenticationFailed("Invalid credentials")


def auth_headers_jwt(token: str) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return headers


def auth_refresh(user: User) -> dict[str, str]:
    if isinstance(user, User):
        refresh_token(user=user)
        return {
            "access_token": access_token(user=user),
            "refresh_token": str(
                cache.get(name=f"refresh_token_{user.id}").decode("utf-8")
            ),
        }
    raise exceptions.AuthenticationFailed("Invalid credentials")


def auth_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return {"detail": "Successfully logged out"}
    else:
        raise exceptions.ValidationError("User is not logged in")
