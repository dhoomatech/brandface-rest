from rest_framework import serializers
from rest_framework import viewsets, status
from .models import ProfileLinks
from email.policy import default
from rest_framework import serializers
from rest_framework import viewsets, status
from .models import *
# from django_countries.serializers import CountryFieldMixin
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction

class ProfileLinkSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    user = serializers.CharField(required=True)
    background = serializers.ImageField(required=False)
    gallery_id = serializers.ListField(child=serializers.CharField(), required=False)
    social_media = serializers.ListField(child=serializers.JSONField(), required=False)
    class Meta:
        model = ProfileLinks
        exclude = ['status']
        validators = [
            UniqueTogetherValidator(
                queryset=ProfileLinks.objects.all(),
                fields=['tittle', 'phone_number']
            )
        ]
    
    def create(self, validated_data):
        instants = None
        try:
            with transaction.atomic():
                gallery_id = None
                if 'gallery_id' in validated_data:
                    gallery_id = validated_data.pop("gallery_id")

                social_media = None
                if 'social_media' in validated_data:
                    social_media = validated_data.pop("social_media")
                    
                validated_data['user'] = User.objects.filter(id=validated_data["user"]).first()
                instance = super().create(validated_data)

                if instance:
                    instance_id = instance.id
                    import ast
                    if gallery_id:
                        gallery_id = ast.literal_eval(gallery_id[0])
                        UserGallery.objects.filter(id__in=gallery_id).update(profile=instance_id)
                    
                    if social_media:
                        social_media_list = []
                        social_media = ast.literal_eval(social_media[0])
                        for socialobj in social_media:
                            social_media_list.append(UserConnections(profile_id=instance_id,social_id=socialobj['id'],value=socialobj['value']))

                        if social_media_list:
                            UserConnections.objects.bulk_create(social_media_list)

                return instance
        
        except Exception as e:
            import traceback
            traceback.print_exc()

        return instants
    
    def update(self, instance, validated_data):
        try:
            # Update the avatar if provided
            if 'avatar' in validated_data:
                instance.avatar = validated_data['avatar']
            
            if 'background' in validated_data:
                instance.avatar = validated_data['background']

            instance.save()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
        
        return instance

class ProfileLinksCreateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    user = serializers.CharField(required=False)
    background = serializers.ImageField(required=False)
    gallery_id = serializers.ListField(child=serializers.CharField(), required=False)
    social_media = serializers.ListField(child=serializers.JSONField(), required=False)

    class Meta:
        model = ProfileLinks
        exclude = ['status']
        validators = [
            UniqueTogetherValidator(
                queryset=ProfileLinks.objects.all(),
                fields=['tittle', 'phone_number']
            )
        ]
    
    def validate(self, data):
        # if data['start_date'] > data['end_date']:
        #     raise serializers.ValidationError("finish must occur after start")
        return data
    
    def update(self, instance, validated_data):
        try:
            # Update the avatar if provided
            if 'avatar' in validated_data:
                instance.avatar = validated_data['avatar']
            
            if 'background' in validated_data:
                instance.avatar = validated_data['background']

            gallery_id = None
            if 'gallery_id' in validated_data:
                gallery_id = validated_data.pop("gallery_id")

            social_media = None
            if 'gallery_id' in validated_data:
                social_media = validated_data.pop("social_media")

            instance.save()
            
            if instance:
                instance_id = instance.id
                if gallery_id:
                    UserGallery.objects.filter(id__in=gallery_id).update(profile=instance_id)
                
                if social_media:
                    social_media_list = []
                    for socialobj in social_media:
                        social_media_list.append(UserConnections(profile_id=instance_id,social_id=socialobj['id'],value=socialobj['value']))

                    if social_media_list:
                        UserConnections.objects.bulk_create(social_media_list) 
            
        except Exception as e:
            import traceback
            traceback.print_exc()
        
        return instance


class ProfileLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        exclude = ['id','user','qr_file','username','status']
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
        exclude = ['created','profile']

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