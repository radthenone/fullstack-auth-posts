from apps.users.models import User
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class Validators:
    @staticmethod
    def validate_email(email: str):
        user = get_object_or_404(User, email=email)
        return user.email


class FriendRequestSerializer(serializers.Serializer):
    friend_email = serializers.EmailField(required=True)

    @staticmethod
    def validate_friend_email(value):
        return Validators.validate_email(email=value)

    def create(self, validated_data):
        sender_email = self.context.get("sender_email")
        token = self.context.get("email_token")
        friend_email = validated_data.get("friend_email")
        url = f"{settings.DOMAIN_URL}/api/users/friend/response/{token}"
        friend_model = get_object_or_404(User, email=friend_email)
        friend_emails = [user.email for user in friend_model.friends.all()]

        if sender_email == friend_email:
            raise serializers.ValidationError("It's your email")

        if sender_email in friend_emails:
            raise serializers.ValidationError(f"{friend_email} is already your friend.")

        if sender_email in friend_model.friend_requests:
            raise serializers.ValidationError(
                f"{sender_email} has already sent you a friend request."
            )

        with transaction.atomic():
            friend_model.friend_requests[sender_email] = url
            friend_model.save()

        return validated_data


class FriendResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("friend_requests",)


class FriendResponseDetailSerializer(serializers.Serializer):
    choice = serializers.ChoiceField(choices=["Yes", "No"], write_only=True)
