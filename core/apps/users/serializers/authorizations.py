from rest_framework import serializers
from apps.users.models import User, RegisterToken
from apps.users.tasks import send_confirmation_email
from apps.users.serializers.serializer import UserSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email_token = serializers.UUIDField(read_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, )

    @staticmethod
    def validate_passwords(password1, password2):
        if password1 and password2 and password2 != password1:
            return serializers.ValidationError("Passwords don't match, try again")
        else:
            return password1

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        attrs['password'] = self.validate_passwords(password1, password2)
        return attrs

    def create(self, validated_data):
        validated_data['email_token'] = RegisterToken.objects.create().token
        send_confirmation_email.delay(validated_data['email'], validated_data['email_token'])
        user = User.objects.create(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        user.set_password(user.password)
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop('user', {})
        representation.update(user_representation)
        return representation

    class Meta:
        model = User
        fields = ('email', 'roles', 'password', 'password2', 'email_token')
        extra_kwargs = {
            'password': {'write_only': True},
            'roles': {'read_only': True},
            'email_token': {'read_only': True},
        }
