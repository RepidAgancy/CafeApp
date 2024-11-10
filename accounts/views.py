from rest_framework import response, generics, status, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import serializers
from accounts.models import Profession, User


class LogOutView(generics.GenericAPIView):
    """
    Bu Api Refresh token qabul qiladi va Tokenni blacklistga qoshib qoyadi
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        try:
            refresh = request.data['refresh_token']
            token = RefreshToken(refresh)
            token.blacklist()
            return response.Response({"message":"User successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"message":f"Error occured {e}"})


class ProfessionListAPIView(generics.ListAPIView):
    serializer_class = serializers.ProfessionListSerializer
    queryset = Profession.objects.all()
    permission_classes = (permissions.AllowAny,)


class UserTypeListApiView(views.APIView):
    def get(self, request):
        data = {
            'user_type': User.get_user_type_list()
        }
        return response.Response(data)


