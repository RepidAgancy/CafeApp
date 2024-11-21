from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
        if not user.check_password(password):
            raise serializers.ValidationError({'detail': 'No active account found with the given '})
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        token = RefreshToken.for_user(user)
        data = {
            'user_type': user.type if hasattr(user, 'type') else None,
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


