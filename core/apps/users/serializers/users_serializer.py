from apps.users.models import Profile, User, UserBasic, UserPremium
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators


class Validator:
    @staticmethod
    def validate_passwords(values):
        password = values.get("password")
        password2 = values.get("password2")
        if password != password2:
            raise validators.ValidationError("Passwords don't match, try again")
        return values


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=False,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )
    username = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    roles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    friends = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "friends",
            "roles",
        )

    @classmethod
    def get_username(cls, instance) -> str:
        return instance.username.split("_")[0]

    def validate(self, attrs):
        Validator.validate_passwords(attrs)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.full_clean()
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    created_at_date = serializers.DateTimeField(
        format="%d-%m-%Y",
        source="created_at",
        read_only=True,
    )
    created_at_time = serializers.DateTimeField(
        format="%H:%M",
        source="created_at",
        read_only=True,
    )
    updated_at_date = serializers.DateTimeField(
        format="%d-%m-%Y",
        source="updated_at",
        read_only=True,
    )
    updated_at_time = serializers.DateTimeField(
        format="%H:%M",
        source="updated_at",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            "user",
            "avatar",
            "created_at_date",
            "created_at_time",
            "updated_at_date",
            "updated_at_time",
            "birth_date",
            "is_premium",
            "is_basic",
            "age",
        )
        read_only_fields = (
            "is_basic",
            "is_premium",
            "age",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = representation.pop("user", None)
        representation.update(user)
        return representation

    def update(self, instance, validated_data):
        user_validated_data = validated_data.pop("user", None)
        user = instance.user

        if user_validated_data is not None:
            self.fields["user"].update(user, user_validated_data)

        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.full_clean()
        instance.save()
        return instance


class BasicUserSerializer(ProfileSerializer):
    class Meta:
        model = UserBasic
        fields = ProfileSerializer.Meta.fields + (
            "is_basic",
            "is_premium",
        )
        read_only_fields = ProfileSerializer.Meta.read_only_fields


class PremiumUserSerializer(ProfileSerializer):
    class Meta:
        model = UserPremium
        fields = ProfileSerializer.Meta.fields + (
            "is_basic",
            "is_premium",
        )
        read_only_fields = ProfileSerializer.Meta.read_only_fields
