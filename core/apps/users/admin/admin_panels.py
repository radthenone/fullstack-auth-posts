from django.contrib import admin
from django.contrib.auth.models import Group

from apps.users.models import Profile, User, UserBasic, UserPremium

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')


class CustomForBasicAndPremium(admin.ModelAdmin):
    list_display = (
        'get_username', 'is_basic', 'is_premium', 'get_email', 'get_password', 'avatar',
    )
    readonly_fields = ('get_username', 'is_basic', 'is_premium',)

    @classmethod
    def get_username(cls, obj):
        return obj.user.username

    @classmethod
    def get_email(cls, obj):
        return obj.user.email

    @classmethod
    def get_password(cls, obj):
        return obj.user.password


@admin.register(UserBasic)
class UserBasicAdmin(CustomForBasicAndPremium):
    pass


@admin.register(UserPremium)
class UserPremiumAdmin(CustomForBasicAndPremium):
    pass


admin.site.unregister(Group)
