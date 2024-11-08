from rest_framework import response, generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import serializers

class LogOutView(generics.GenericAPIView):
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

