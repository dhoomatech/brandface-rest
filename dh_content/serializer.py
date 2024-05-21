from rest_framework import serializers
from rest_framework import viewsets, status
from .models import ProfileLinks
from email.policy import default
from rest_framework import serializers
from rest_framework import viewsets, status
from .models import *
from django_countries.serializers import CountryFieldMixin

class ProfileLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        exclude = ['id','user']


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