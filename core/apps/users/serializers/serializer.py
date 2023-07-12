from apps.users.models import User, UserBasic
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "full_name",
            "roles",
        )

    @classmethod
    def get_username(cls, obj) -> str:
        return obj.username.split("_")[0]


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBasic
        fields = (
            "is_basic",
            "is_premium",
        )
