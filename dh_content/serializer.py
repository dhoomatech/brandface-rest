from rest_framework import serializers
from rest_framework import viewsets, status
from .models import ProfileLinks
from email.policy import default
from rest_framework import serializers
from rest_framework import viewsets, status
from .models import *
from django_countries.serializers import CountryFieldMixin
from rest_framework.validators import UniqueTogetherValidator

class ProfileLinksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        exclude = ['status']
        validators = [
            UniqueTogetherValidator(
                queryset=ProfileLinks.objects.all(),
                fields=['tittle', 'phone_number']
            )
        ]

class ProfileLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        exclude = ['id','user','qr_file','username']
        validators = [
            UniqueTogetherValidator(
                queryset=ProfileLinks.objects.all(),
                fields=['tittle', 'phone_number']
            )
        ]


class ProfileLinkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        fields = ['user','avatar','background']


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ['status']

class UserGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGallery
        exclude = ['created']

class UserServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServices
        fields = '__all__'
    
class UserConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnections
        exclude = ['status']


class ProfileReadSerializer(serializers.ModelSerializer):
    gallary_data = serializers.SerializerMethodField(read_only=True)
    social_data = serializers.SerializerMethodField(read_only=True)
    def get_gallary_data(self, obj):
        user_gallary_data = list(UserGallery.objects.filter(profile=obj).values("id","picture").all())
        return user_gallary_data 
    
    def get_social_data(self, obj):
        social_data = list(UserConnections.objects.filter(profile=obj).values("social__name","value").all())
        return social_data
     
    class Meta:
        model = ProfileLinks
        exclude = ['id','user','status']