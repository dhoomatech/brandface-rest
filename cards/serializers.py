from rest_framework import serializers
from .models import *



class ThemeTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThemeTemplate
        fields = ['id', 'name', 'description', 'preview_image', 'theme_setting']

class ThemeSettingSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='theme_template.name', read_only=True)
    class Meta:
        model = ThemeSetting
        fields = '__all__'


class TrackingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingConfig
        fields = '__all__'

class SocialMediaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPlatform
        fields = ['name', 'icon']
        read_only_fields = fields  # make all fields read-only

class SocialMediaSerializer(serializers.ModelSerializer):
    platform = SocialMediaPlatformSerializer(read_only=True)
    class Meta:
        model = SocialMedia
        exclude = ['id','profile']

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
        fields = '__all__'

class ProfileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSettings
        fields = '__all__'

class BusinessProfileSerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    gallery = GalleryImageSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    seo = BusinessProfileSEOSerializer(read_only=True)
    tracking = TrackingConfigSerializer(read_only=True)
    profile_setting = serializers.SerializerMethodField()
    theme_setting = serializers.SerializerMethodField()
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ['owner']
    
    def get_theme_setting(self, obj):
        setting = ThemeSetting.objects.filter(profile=obj).first()
        return ThemeSettingSerializer(setting).data if setting else {}

    def get_profile_setting(self, obj):
        setting = ProfileSettings.objects.filter(profile=obj).first()
        return ProfileSettingsSerializer(setting).data if setting else {}


class BusinessProfileViewSerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    gallery = GalleryImageSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    seo = BusinessProfileSEOSerializer(read_only=True)
    tracking = TrackingConfigSerializer(read_only=True)
    profile_setting = serializers.SerializerMethodField()
    theme_setting = serializers.SerializerMethodField()
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ['owner']
    
    def get_theme_setting(self, obj):
        setting = ThemeSetting.objects.filter(profile=obj).first()
        return ThemeSettingSerializer(setting).data if setting else {}

    def get_profile_setting(self, obj):
        setting = ProfileSettings.objects.filter(profile=obj).first()
        return ProfileSettingsSerializer(setting).data if setting else {}
    
class SocialMediaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPlatform
        fields = ['id', 'name', 'icon']