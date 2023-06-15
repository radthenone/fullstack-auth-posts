from django.contrib import admin
from apps.users.models import UserBasic, UserPremium
from django.contrib.auth.models import Group
from django.contrib import admin

# Register your models here.


@admin.register(UserBasic)
class UserBasicAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPremium)
class UserPremiumAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
