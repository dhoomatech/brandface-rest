from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('user/upload-profile-image/', ProfileImageUpdateAPIView.as_view(), name='upload-profile-image'),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path("change-password", ChangePassword.as_view(), name="change-password"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('initiate-forget-password', InititeForgetPassword.as_view(), name='initiate-reset-password'),
    path('complete-forget-password', ForgetPasswordView.as_view(), name='complete-reset-password'),

    
]
