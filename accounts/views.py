from rest_framework.response import Response
from rest_framework import response, generics, status, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import serializers
from accounts.models import User
from accounts.serializers import UserProfileSerializer
from crm.serializers import UserListSerializer


class LoginApiView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UserTypeListApiView(views.APIView):
    def get(self, request):
        data = {
            'user_type': User.get_user_type_list()
        }
        return response.Response(data)


class UserProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer
    pagination_class = None
    def get(self, request):
        user_serializer = self.serializer_class(instance=request.user)
        return response.Response(user_serializer.data)


