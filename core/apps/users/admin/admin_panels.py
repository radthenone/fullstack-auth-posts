from apps.users.models import EmailSend, RegisterToken, User, UserBasic, UserPremium
from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(EmailSend)
class EmailSendAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "message",
        "from_email",
        "get_recipient_list",
        "fail_silently",
    )

    def get_recipient_list(self, obj):
        return ", ".join(obj.recipient_list)

    get_recipient_list.short_description = "Recipient List"


@admin.register(RegisterToken)
class RegisterTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "url_used", "created_at", "get_email")

    @classmethod
    def get_email(cls, obj):
        return obj.user.email


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")


class CustomForBasicAndPremium(admin.ModelAdmin):
    list_display = (
        "get_username",
        "is_basic",
        "is_premium",
        "get_email",
        "get_password",
        "avatar",
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


@admin.register(UserBasic)
class UserBasicAdmin(CustomForBasicAndPremium):
    pass


@admin.register(UserPremium)
class UserPremiumAdmin(CustomForBasicAndPremium):
    pass


admin.site.unregister(Group)
