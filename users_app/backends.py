from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import BlacklistedAccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings

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

        for path in settings.PUBLIC_PATHS:
            if request.path.startswith(path):
                return None  # Skip JWT check

        # ✅ Bypass JWT if the view allows AllowAny
        try:
            if request.resolver_match:
                view_func = request.resolver_match.func
                view_class = getattr(view_func, 'view_class', None)
                if view_class:
                    view = view_class()
                    view.request = request
                    view.args = ()
                    view.kwargs = request.resolver_match.kwargs

                    # ✅ This is the correct way to get active permissions
                    permissions = view.get_permissions()
                    if any(isinstance(p, AllowAny) for p in permissions):
                        return None
        except Exception:
            pass  # Fail gracefully and proceed with authentication

        # ✅ JWT validation continues here
        header = self.get_header(request)
        if header is None:
            raise AuthenticationFailed({
                "status": "failed",
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Authentication credentials not provided"
            })

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise AuthenticationFailed({
                "status": "failed",
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid token format"
            })

        try:
            validated_token = self.get_validated_token(raw_token)
            jti = validated_token.get("jti")
        except (InvalidToken, TokenError):
            raise AuthenticationFailed({
                "status": "failed",
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid or expired authentication token"
            })

        if jti and BlacklistedAccessToken.objects.filter(token_jti=jti).exists():
            raise AuthenticationFailed({
                "status": "failed",
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Token has been blacklisted. Please log in again."
            })

        return self.get_user(validated_token), validated_token