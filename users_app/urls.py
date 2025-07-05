from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/register/', RegisterView.as_view()),
    path('v1/user/upload-profile-image/', ProfileImageUpdateAPIView.as_view(), name='upload-profile-image'),


    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/login/', CustomLoginView.as_view(), name='custom_login'),
    path("v1/change-password", ChangePassword.as_view(), name="change-password"),
    path('v1/logout', LogoutView.as_view(), name='logout'),
    path('v1/initiate-forget-password', InititeForgetPassword.as_view(), name='initiate-reset-password'),
    path('v1/complete-forget-password', ForgetPasswordView.as_view(), name='complete-reset-password'),

    
]
