from rest_framework import serializers
from .models import BusinessProfile, SocialMedia, Service, GalleryImage, SocialMediaPlatform, PhoneNumber, BusinessProfileSEO

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

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number']

class BusinessProfileSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfileSEO
        fields = [
            'meta_title',
            'meta_description',
            'meta_keywords',
            'og_title',
            'og_description',
            'og_image',
        ]

class BusinessProfileSerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    gallery = GalleryImageSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    seo = BusinessProfileSEOSerializer(read_only=True)
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ['owner']

class SocialMediaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPlatform
        fields = ['id', 'name', 'icon']