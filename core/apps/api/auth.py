from apps.users.models import User
from rest_framework import serializers, validators
from apps.users.serializers import Validator as UserValidator
from django.contrib.auth.password_validation import validate_password
from apps.api.utils import encode_token, decode_token
from django.conf import settings
from apps.emails.tasks import send_register_email


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2", "email_token")

    def validate(self, attrs):
        UserValidator.validate_passwords(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        payload = {
            "email": validated_data.get("email"),
            "password": validated_data.get("password"),
        }
        exp_minutes = 30
        token = encode_token(payload=payload, exp_minutes=exp_minutes)
        data = {
            "email": validated_data.get("email"),
            "message": {
                "title": "Register",
                "email": validated_data.get("email"),
                "auth_url": f"{settings.DOMAIN_URL}/auth/{token}/",
                "info": f"Kindly use this token to verify your email. \
        Only valid for {exp_minutes} minutes.",
            },
        }
        send_register_email.delay(**data)
