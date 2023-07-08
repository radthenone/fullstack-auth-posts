from typing import Any

from apps.users.views import RegisterView, UserViewDetail, UserViewList
from django.urls import path

urlpatterns: Any = [
    path("register/", RegisterView.as_view(), name="register"),
    path("<int:pk>", UserViewDetail.as_view(), name="user-detail"),
    path("", UserViewList.as_view(), name="user-list"),
]
