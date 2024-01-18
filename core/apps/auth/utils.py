import datetime
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import HttpRequest
from rest_framework import exceptions

from apps.api.tokens import encode_token
from apps.users.models import User
from redis.exceptions import RedisError


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
    try:
        cache.set(
            key=f"refresh_{str(user.id)}",
            value=encode_token(
                payload=payload,
                exp_days=14,
                key=settings.SIMPLE_JWT["REFRESH_KEY"],
            ),
            timeout=datetime.timedelta(days=14).total_seconds(),
        )
    except RedisError as error:
        raise exceptions.ValidationError(error)


def auth_login(request: HttpRequest, email: str, password: str) -> dict[str, str]:
    user = authenticate(email=email, password=password)
    if isinstance(user, User):
        login(request, user)
        refresh_token(user=user)
        return {
            "access": access_token(user=user),
            "refresh": str(
                cache.get(
                    key=f"refresh_{user.id}",
                )
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
            "access": access_token(user=user),
            "refresh": str(
                cache.get(
                    key=f"refresh_{user.id}",
                )
            ),
        }
    raise exceptions.AuthenticationFailed("Invalid credentials")


def auth_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return {"detail": "Successfully logged out"}
    else:
        raise exceptions.ValidationError("User is not logged in")
