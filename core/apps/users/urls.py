from typing import Any

from django.urls import path

from apps.users.views import (
    FriendRequestView,
    FriendResponseDetailView,
    FriendResponseView,
    RolesDetailView,
    RolesListView,
    UserDetailView,
    UserListView,
)

urlpatterns: Any = [
    # users
    path("", UserListView.as_view(), name="user-list"),
    path("detail/", UserDetailView.as_view(), name="user-detail"),
    # friends
    path(
        "friend/request/",
        FriendRequestView.as_view(),
        name="friend-request",
    ),
    path(
        "friend/response/",
        FriendResponseView.as_view(),
        name="friend-response-list",
    ),
    path(
        "friend/response/<str:friend_token>/",
        FriendResponseDetailView.as_view(),
        name="friend-response-detail",
    ),
    # roles
    path("roles/", RolesListView.as_view(), name="role-list"),
    path("roles/<str:name>/", RolesDetailView.as_view(), name="role-detail"),
]
