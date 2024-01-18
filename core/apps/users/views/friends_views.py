from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from apps.api.tokens import decode_token, encode_token
from apps.users.models import Friendship
from apps.users.serializers import (
    FriendRequestSerializer,
    FriendResponseDetailSerializer,
    FriendResponseSerializer,
)
from apps.users.types import UserModelType


class FriendRequestView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer
    tag_name = "friends"

    @extend_schema(
        tags=[tag_name],
        description="Posts a friend",
        request=FriendRequestSerializer,
        responses={
            status.HTTP_201_CREATED: None,
        },
    )
    def post(self, request, *args, **kwargs):
        sender_email = request.user.email
        friend_email = request.data.get("friend_email")
        payload = {
            "sender_email": sender_email,
            "friend_email": friend_email,
        }
        email_token = encode_token(payload=payload, exp_hours=3)
        serializer = self.serializer_class(
            data=request.data,
            context={
                "sender_email": sender_email,
                "email_token": email_token,
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Friend request sent"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class FriendResponseView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = FriendResponseSerializer
    tag_name = "friends"

    def get_queryset(self):
        users = (
            get_user_model()
            .objects.prefetch_related("friends")
            .filter(email=self.request.user)
        )
        return users

    @extend_schema(
        tags=[tag_name],
        description="Get friend list",
        request=FriendResponseSerializer,
        responses={
            status.HTTP_200_OK: FriendResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        friend_requests_links = [
            user.get_friends_response_url(token)
            for user in serializer.data
            for token in user["friend_requests"].values()
        ]
        return Response(friend_requests_links, status=status.HTTP_200_OK)


class FriendResponseDetailView(
    generics.GenericAPIView,
):
    serializer_class = FriendResponseDetailSerializer
    tag_name = "friends"

    @extend_schema(
        tags=[tag_name],
        description="Posts a friend",
        request=FriendResponseDetailSerializer,
        responses={
            status.HTTP_200_OK: FriendResponseDetailSerializer,
        },
    )
    def post(self, request, friend_token):
        choice = request.data.get("choice")
        user = get_object_or_404(get_user_model(), email=request.user.email)
        payload = decode_token(
            token=friend_token,
        )
        if "errors" in payload:
            return Response(
                {"errors": payload["errors"]}, status=status.HTTP_400_BAD_REQUEST
            )
        if payload is not None and request.user.email == payload.get("friend_email"):
            sender = get_object_or_404(
                get_user_model(), email=payload.get("sender_email")
            )
            if sender in user.friends.prefetch_related("friends"):
                return Response(
                    {"detail": f"Friend from {sender.email} is already your friend"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if choice == "Yes":
                    self.handle_accept_request(user, sender)
                    return Response(
                        data={"detail": f"Friend from {sender.email} request accepted"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    self.handle_reject_request(user, sender)
                    return Response(
                        data={"detail": f"Friend from {sender.email} request rejected"},
                        status=status.HTTP_200_OK,
                    )

        return Response({"errors": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handle_accept_request(user: "UserModelType", sender: "UserModelType"):
        friendship = Friendship.objects.add_friend(from_user=sender, to_user=user)
        friendship.is_accepted = True
        friendship.save()
        user.friends.add(friendship, through_defaults={})
        if sender.email in user.friend_requests:
            del user.friend_requests[sender.email]
            user.save()

    @staticmethod
    def handle_reject_request(user: "UserModelType", sender: "UserModelType"):
        if sender.email in user.friend_requests:
            del user.friend_requests[sender.email]
            user.save()
