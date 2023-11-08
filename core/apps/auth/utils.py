from apps.api.tokens import encode_token
from apps.users.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest


def access_token(email: str) -> str:
    user = User.objects.get_object_by_email(email=email)
    if not user:
        raise ValueError("Invalid credentials")
    payload = {
        "token_type": "access",
        "user_id": str(user.id),
        "user_email": user.email,
    }
    return encode_token(payload=payload, exp_minutes=10)


def refresh_token(email: str) -> str:
    user = User.objects.get_object_by_email(email=email)
    if not user:
        raise ValueError("Invalid credentials")
    payload = {
        "token_type": "refresh",
        "user_id": str(user.id),
        "user_email": user.email,
    }
    return encode_token(payload=payload, exp_days=14)


def auth_login(request: HttpRequest, email: str, password: str) -> dict[str, str]:
    user = authenticate(email=email, password=password)
    if user:
        login(request, user)
        return {
            "access_token": access_token(email=email),
            "refresh_token": refresh_token(email=email),
        }
    raise ValueError("Invalid credentials")


def auth_headers_jwt(token: str) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return headers


def auth_refresh(request: HttpRequest) -> dict[str, str]:
    if isinstance(request.user, User):
        return {"access_token": access_token(email=request.user.email)}
    raise ValueError("Invalid credentials")


def auth_logout(request: HttpRequest):
    logout(request)
    return {"detail": "Successfully logged out"}
