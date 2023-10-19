from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import generics, permissions, mixins, status
from apps.api.tokens import encode_token, decode_token
from apps.users.serializers import (
    FriendRequestSerializer,
    FriendResponseSerializer,
    FriendResponseDetailSerializer,
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class FriendRequestView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

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

    def get_queryset(self):
        users = (
            get_user_model()
            .objects.prefetch_related("friends")
            .filter(email=self.request.user)
        )
        return users

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        friend_requests_links = [
            value
            for user in serializer.data
            for value in user["friend_requests"].values()
        ]
        return Response(friend_requests_links, status=status.HTTP_200_OK)


class FriendResponseDetailView(
    generics.GenericAPIView,
):
    serializer_class = FriendResponseDetailSerializer

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
        if payload is not None:
            if request.user.email == payload.get("friend_email"):
                sender_email = payload.get("sender_email")
                sender = get_object_or_404(get_user_model(), email=sender_email)
                if sender in user.friends.prefetch_related("friends"):
                    return Response(
                        {
                            "detail": f"Friend from {sender_email} is already your friend"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    if choice == "Yes":
                        self.handle_accept_request(user, sender, sender_email)
                        return Response(
                            data={
                                "detail": f"Friend from {sender_email} request accepted"
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        self.handle_reject_request(user, sender_email)
                        return Response(
                            data={
                                "detail": f"Friend from {sender_email} request rejected"
                            },
                            status=status.HTTP_200_OK,
                        )

        return Response({"errors": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handle_expired_token(user, friend_token):
        tokens_to_remove = []
        for friend_email, friend_url in user.friend_requests.items():
            if friend_url.endswith(friend_token):
                tokens_to_remove.append(friend_email)
        for email in tokens_to_remove:
            del user.friend_requests[email]
            user.save()

    @staticmethod
    def handle_accept_request(user, sender, sender_email):
        user.friends.add(sender)
        if sender_email in user.friend_requests:
            del user.friend_requests[sender_email]
            user.save()

    @staticmethod
    def handle_reject_request(user, sender_email):
        if sender_email in user.friend_requests:
            del user.friend_requests[sender_email]
            user.save()
