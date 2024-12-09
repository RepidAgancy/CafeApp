from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework import response, generics, status, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken
from crm import permissions as permission

from accounts import serializers
from accounts.models import User
from accounts.serializers import UserProfileSerializer


class LoginApiView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_200_OK)


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
    @method_decorator(cache_page(60*1000))
    def get(self, request):
        data = {
            'user_type': User.get_user_type_list()
        }
        return response.Response(data)


class UserProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer
    pagination_class = None

    @method_decorator(cache_page(60*5))
    def get(self, request):
        user_serializer = self.serializer_class(instance=request.user)
        return response.Response(user_serializer.data)


class UserProfileChangeView(generics.UpdateAPIView):
    permission_classes = (permission.IsAdminUser,)  
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
