from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from apps.api.tokens import encode_token
from apps.emails.utils import CreateMail
from apps.files.fields import ResizeBase64ImageField
from apps.users.models import Roles, User, UserBasic
from apps.users.serializers import Validator as UserValidator


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
                "token": token,
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
    user = RegisterUserSerializer(many=False, required=True)
    avatar = ResizeBase64ImageField(
        required=False,
        size=(200, 200),
    )

    class Meta:
        model = UserBasic
        fields = (
            "user",
            "avatar",
            "birth_date",
        )

    def create(self, validated_data):
        try:
            user_data = validated_data.pop("user")
            user = User.objects.create(
                email=user_data.get("email"),
                change_password=True,
                password=user_data.get("password"),
            )
            user.save()
            user.roles.set([Roles.objects.get_basic_queryset()])
            if user:
                try:
                    basic_user = UserBasic.objects.create(
                        user=user,
                        avatar=validated_data.get("avatar"),
                        birth_date=validated_data.get("birth_date"),
                    )
                    basic_user.save()
                    return basic_user
                except Exception as error:
                    raise serializers.ValidationError({"errors": f"{error}"})
            else:
                raise serializers.ValidationError({"errors": "User does not exist"})
        except Exception as error:
            raise serializers.ValidationError({"errors": f"{error}"})


class LoginRefreshSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")

        if email:
            try:
                user = User.objects.get(email=email)
                exp_minutes = 10
                attrs["token"] = encode_token(
                    payload={"email": user.email}, exp_minutes=exp_minutes
                )
                attrs["exp_minutes"] = exp_minutes
                return attrs

            except User.DoesNotExist:
                raise serializers.ValidationError({"errors": "User does not exist"})
        else:
            raise serializers.ValidationError({"errors": "Email is required"})


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
