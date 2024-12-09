from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = cache.get(f"user_{username}")

        if not user:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
            cache.set(f"user_{username}", user, timeout=300)  # 5 daqiqa kesh

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'User account is disabled'})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        token = RefreshToken.for_user(user)
        return {
            'user_type': getattr(user, 'type', None),
            'refresh': str(token),
            'access': str(token.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'profile_image')

