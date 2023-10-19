from typing import Any

from apps.auth.views import (
    RegisterMailView,
    RegisterView,
)
from django.urls import path

urlpatterns: Any = [
    path("register/", RegisterMailView.as_view(), name="register-mail"),
    path("register/<str:token>/", RegisterView.as_view(), name="register"),
]
