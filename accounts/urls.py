from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

urlpatterns = [
    path('user/login/', TokenObtainPairView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/logout/', views.LogOutView.as_view(), name='logout'),
    path('user/profession/', views.ProfessionListAPIView.as_view(), name='profession_list'),
    path('user/type/list/', views.UserTypeListApiView.as_view(), name='user_type_list'),
]