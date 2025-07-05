from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from users_app.models import *
from users_app.serializers import *
# from users_app.permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from users_app.utils import *



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):    
        serializer.save(role='free_user')

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=OTPLoginSerializer)
    def post(self, request):
        try:
            serializer = OTPLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                "status":"success",
                "response_code":200,"message":"User loggines successfully",
                "user_role":user.role,
                "data":{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }
            )
        except Exception as e:
            message = str(e)
            return Response({"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":message})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        try:
            user = request.user
            data = request.data
            if user.check_password(data['current_password']):
                if data['new_password1'] != data['new_password2']:
                    return Response({"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":"Sorry, password not matching"})
                user.set_password(data['new_password1'])
                user.save()
                return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"Password changed successfully"})
            else:
                return Response({"status":"failed","response_code":status.HTTP_400_BAD_REQUEST,"message":"Current password is incorrect. Please try again later"})
        except Exception  as e:
            message = str(e)
            return Response({"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":message})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        try:
            """to get access token by slicing bearer"""
            access_token = request.headers.get("Authorization", "").split(" ")[1]
            refresh_token = request.data["refresh_token"]
            if not refresh_token:
                raise Exception("Sorry, Refresh token is required")
            token = RefreshToken(refresh_token)
            token.blacklist()
            access_token_obj = AccessToken(access_token)
            # to block access token too, need to handle it in custom token manage class
            BlacklistedAccessToken.objects.create(token_jti=access_token_obj["jti"])
            return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"User logout successfully"})
        except Exception as e:
            message = str(e)
            return Response({"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":message})
                

class InititeForgetPassword(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response({"status":"failed","response_code":status.HTTP_404_NOT_FOUND,"message":"Enter your registered email address"})
        token = default_token_generator.make_token(user)
        PasswordResetToken.objects.create(user=user, token=token)

        # Send email with the reset link (assuming you have email settings configured)
        reset_link = f'{"FORGET_PASSWORD_URL"}/{token}/'
        print(reset_link)

        mail_data = {
            "name":user.first_name,
            "url":reset_link
        }
        send_mail_content("password_reset",mail_data,user.email)
        return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"reset password link sent to mail successfully"})


class ForgetPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        try:
            reset_token = PasswordResetToken.objects.filter(token=token).first()
            if not reset_token:
                return Response({"status":"failed","response_code":status.HTTP_404_NOT_FOUND,"message":"This password reset link has expired or is invalid. Please request a new password reset email"})
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            reset_token.delete()
            return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"Password reset successfully"})

        except Exception as e:
            message = str(e)
            return Response({"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":message})

class ProfileImageUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user