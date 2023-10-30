from apps.users.models import User, UserBasic
from apps.users.serializers import UserSerializer, BasicUserSerializer
from rest_framework import serializers, validators
from apps.users.serializers import Validator as UserValidator
from django.contrib.auth.password_validation import validate_password
from apps.api.tokens import encode_token, decode_token
from django.conf import settings
from apps.emails.utils import CreateMail
from django.contrib.auth.hashers import check_password, make_password


class RegisterMailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    def validate(self, attrs):
        UserValidator.validate_passwords(attrs)
        return attrs

    def create(self, validated_data):
        email, password = validated_data.get("email"), make_password(
            validated_data.get("password")
        )
        payload = {
            "email": email,
            "password": password,
        }
        exp_minutes = 30
        token = encode_token(payload=payload, exp_minutes=exp_minutes)
        mail = CreateMail(
            send_email=email,
            title="Register",
            extra_message={
                "auth_url": f"{settings.DOMAIN_URL}/api/auth/register/{token}/",
            },
            info=f"Kindly use this token to verify your email. \
        Only valid for {exp_minutes} minutes.",
        )
        return mail


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )


class RegisterSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()

    class Meta:
        model = UserBasic
        fields = (
            "user",
            "avatar",
            "birth_date",
        )

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(
            email=email,
            password=password,
        )
        UserBasic.objects.create(
            user=user,
            avatar=validated_data.get("avatar"),
            birth_date=validated_data.get("birth_date"),
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, write_only=True, style={"input_type": "email"}
    )
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
