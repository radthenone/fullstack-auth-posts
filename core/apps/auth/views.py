from rest_framework.response import Response
from rest_framework import generics, status
from apps.auth.serializers import RegisterMailSerializer, RegisterSerializer
from apps.api.tokens import decode_token
from django.contrib.auth.hashers import check_password
from apps.emails.tasks import send_register_email


class RegisterMailView(generics.GenericAPIView):
    serializer_class = RegisterMailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mail = serializer.save()
            send_register_email.delay(**mail)
            return Response(
                data={"detail": "Register email sent"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, token):
        data = decode_token(token)
        if check_password(request.data.get("password"), data.get("password")):
            request.data.update({"email": data.get("email")})
            serializer = self.get_serializer(data=request.data, files=request.files)
            if serializer.is_valid():
                instance = serializer.save()
                email = instance.data.get("email")
                return Response(
                    {"detail": f"User created successfully {email}"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )
