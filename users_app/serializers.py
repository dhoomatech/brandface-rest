from rest_framework import serializers
from users_app.models import *
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class OTPLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Try email lookup
        user = User.objects.filter(email__iexact=email).first()

        if not user:
            # If not email, try username
            user = User.objects.filter(username__iexact=email).first()

        if not user:
            raise serializers.ValidationError("Invalid username or email.")
        
        # Authenticate the user
        authenticated_user = authenticate(
            request=self.context.get('request'),
            username=user.username,  # use username always for authenticate()
            password=password
        )

        if not authenticated_user:
            raise serializers.ValidationError("Incorrect password.")
        
        if not user:
            raise Exception("The credentials you enetered is incorrect")
        attrs['user'] = user
        return attrs
    


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["current_password","new_password1","new_password2"]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']
