from rest_framework import serializers

from accounts.models import Profession


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class ProfessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'name_uz', 'name_ru', 'name_en']