from apps.users.models import Roles
from django_filters import rest_framework as filters


class RolesFilter(filters.FilterSet):
    class Meta:
        model = Roles
        fields = ("name",)
