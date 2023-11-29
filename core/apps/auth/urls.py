from typing import Any

from apps.auth.views import (
    LoginRefreshMailView,
    LoginRefreshView,
    LoginView,
    LogoutView,
    RegisterMailView,
    RegisterView,
)
from django.urls import path

urlpatterns: Any = [
    path("register/", RegisterMailView.as_view(), name="register-mail"),
    path("register/<str:token>/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/refresh/<str:token>/",
        LoginRefreshView.as_view(),
        name="login-refresh",
    ),
    path("login/refresh/", LoginRefreshMailView.as_view(), name="login-refresh-mail"),
]
