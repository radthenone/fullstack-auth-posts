from apps.users.serializers import RegisterSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.save()
            return Response(
                {"message": "Email sent", "email": email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    pass
