from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import BlacklistedAccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    

class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        """
        Custom JWT authentication that:
        - Allows public APIs (with `AllowAny` permission) to proceed without a token.
        - Returns a custom error message if the token is invalid or expired.
        """
        # Check if the view allows public access
        if request.resolver_match is not None:
            view = request.resolver_match.func.view_class
            if hasattr(view, "permission_classes") and AllowAny in view.permission_classes:
                return None 
            
        # Get Authorization header
        header = self.get_header(request)
        error_response = {"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":"Sorry, Authentication credentials not provided"}

        # If the token is missing in a private API, return a custom response
        if header is None:
            raise AuthenticationFailed(error_response)
        raw_token = self.get_raw_token(header)

        # If the token is not found, return a custom error
        if raw_token is None:
            raise AuthenticationFailed(error_response)
        
        error_response = {"status":"failed","response_code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":"Sorry, Invalid authentication credentials provided"}
        try:
            validated_token = self.get_validated_token(raw_token)
            # extracting unique value from token
            jti = validated_token["jti"]
        except (InvalidToken, TokenError):
            raise AuthenticationFailed(error_response)
        
        # checking if access token in blacklisted or not
        if BlacklistedAccessToken.objects.filter(token_jti=jti):
            error_response = {
                "status": "failed",
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Sorry, this token has been blacklisted. Please log in again.",
            }
            raise AuthenticationFailed(error_response)
        return self.get_user(validated_token), validated_token
    
    