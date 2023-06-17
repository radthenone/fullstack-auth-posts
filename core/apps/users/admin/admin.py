from django.contrib import admin
from apps.users.models import UserBasic, UserPremium
from django.contrib.auth.models import Group
from apps.users.models import User, Profile
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')


@admin.register(UserBasic)
class UserBasicAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'is_basic', 'avatar', 'is_premium', 'get_email', 'get_password')

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_password(self, obj):
        return obj.user.password

    get_username.short_description = 'Username'
    get_email.short_description = 'Email'
    get_password.short_description = 'Password'


@admin.register(UserPremium)
class UserPremiumAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
