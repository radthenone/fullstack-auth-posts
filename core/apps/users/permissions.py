from rest_framework import permissions


class IsPremiumPermission(permissions.BasePermission):  # noqa
    def has_object_permission(self, request, view, obj):
        if not request.user.is_premium:
            return False
        return True


class IsBasicPermission(permissions.BasePermission):  # noqa
    def has_object_permission(self, request, view, obj):
        if not request.user.is_basic:
            return False
        return True
