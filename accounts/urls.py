from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

urlpatterns = [
    path('user/login/', views.LoginApiView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/logout/', views.LogOutView.as_view(), name='logout'),
    path('user/type/list/', views.UserTypeListApiView.as_view(), name='user_type_list'),
    path('user/profile/<int:id>/', views.UserProfileView.as_view(), name='user_profile'),
]