from django_filters import rest_framework as filters

from apps.users.models import Roles


class RolesFilter(filters.FilterSet):
    class Meta:
        model = Roles
        fields = ("name",)
