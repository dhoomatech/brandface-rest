from rest_framework import serializers
from .models import BusinessProfile, SocialMedia, Service, GalleryImage

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'
        read_only_fields = ['profile']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['profile']

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = '__all__'
        read_only_fields = ['profile']

class BusinessProfileSerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    gallery = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ['owner']
