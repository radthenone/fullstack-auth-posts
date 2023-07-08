from apps.users.models import EmailSend, RegisterToken, User
from apps.users.tasks import send_confirmation_email
from django.conf import settings
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    email_token = serializers.UUIDField(read_only=True)
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    @staticmethod
    def validate_passwords(password1, password2):
        if password1 and password2 and password2 != password1:
            raise serializers.ValidationError("Passwords don't match, try again")
        return password1

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        attrs["password"] = self.validate_passwords(password1, password2)
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get("email"), password=validated_data.get("password")
        )
        user.set_password(user.password)
        user.save()
        token = RegisterToken.objects.create(user=user).token
        email_send = EmailSend.objects.create(
            subject="Auth Email Register",
            message=f"""
            Click link to confirm:\n
            http://localhost:8000/api/users/confirm_auth/{token}
            """,
            from_email=settings.DEFAULT_EMAIL,
            recipient_list=[
                validated_data.get("email"),
            ],
        )
        email_send.save()
        send_confirmation_email.delay(
            sender_email=email_send.from_email,
            receiver_email=email_send.recipient_list[0],
            add_subject=email_send.subject,
            message=email_send.message,
        )
        return user.email

    class Meta:
        model = User
        fields = ("email", "password", "password2", "email_token")
        extra_kwargs = {
            "password": {"write_only": True},
            "email_token": {"read_only": True},
        }
