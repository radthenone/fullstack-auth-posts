from apps.users.views.friends_views import (
    FriendRequestView,
    FriendResponseDetailView,
    FriendResponseView,
)
from apps.users.views.roles_views import (
    RolesDetailView,
    RolesListView,
)
from apps.users.views.users_views import (
    UserDetailView,
    UserListView,
)

__all__ = (
    "UserDetailView",
    "UserListView",
    "RolesListView",
    "RolesDetailView",
    "FriendRequestView",
    "FriendResponseView",
    "FriendResponseDetailView",
)
