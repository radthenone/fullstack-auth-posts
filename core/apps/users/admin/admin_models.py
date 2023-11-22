from apps.users.admin.admin_forms import UserForm
from apps.users.models import Roles, User, UserBasic, UserPremium
from django.contrib import admin
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        "id",
        "username",
        "email",
        "password",
        "get_roles",
        "get_friends",
        "friend_requests",
    )

    @classmethod
    def get_roles(cls, instance):
        return [role.name for role in instance.roles.all()]

    @classmethod
    def get_friends(cls, instance):
        friend_list = instance.friends.exclude(id=instance.id)
        if friend_list:
            return [friend.email for friend in friend_list]
        return []


class CustomForBasicAndPremium(admin.ModelAdmin):
    list_display = (
        "get_username",
        "is_basic",
        "is_premium",
        "get_email",
        "get_password",
        "avatar",
        "get_roles",
    )
    readonly_fields = (
        "get_username",
        "is_basic",
        "is_premium",
    )

    @classmethod
    def get_username(cls, obj):
        return obj.user.username

    @classmethod
    def get_email(cls, obj):
        return obj.user.email

    @classmethod
    def get_password(cls, obj):
        return obj.user.password

    @classmethod
    def get_roles(cls, obj):
        return [role.name for role in obj.user.roles.all()]


@admin.register(UserBasic)
class UserBasicAdmin(CustomForBasicAndPremium):
    pass


@admin.register(UserPremium)
class UserPremiumAdmin(CustomForBasicAndPremium):
    pass


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
