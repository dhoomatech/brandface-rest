from rest_framework import serializers
from rest_framework import viewsets, status
from .models import User
from email.policy import default
from rest_framework import serializers
from rest_framework import viewsets, status
from .models import *
from django_countries.serializers import CountryFieldMixin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'email_code']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','is_active', 'email_verified', 'email_code']
    
    def to_representation(self, instance):
        return UserSerializer(instance=instance).data

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['email_code']
        extra_kwargs = {'is_admin': {'read_only': True}, 'is_active': {'read_only': True}, 'last_login': {'read_only': True}, 'email_verified': {'read_only': True}, 'password': {'write_only': True},}

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['is_active'] = True
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        return UserSerializer(instance=instance).data

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class AddressReadOnlySerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize Address model
    """

    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class ShippingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type shipping

    For shipping address, automatically set address type to shipping
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "S"

        return representation


class BillingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type billing

    For billing address, automatically set address type to billing
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "B"

        return representation



class PublicIconsCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for categories
    """

    class Meta:
        model = PublicIconsCategory
        fields = "__all__"


class PublicIconsSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading Community
    """
    class Meta:
        model = PublicIcons
        fields = "__all__"


class PublicIconsReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading Community
    """

    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = PublicIcons
        fields = "__all__"

class PublicIconsWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class 
    """

    category = PublicIconsCategoryReadSerializer()

    class Meta:
        model = PublicIcons
        fields = (
            "category",
            "desc",
            "user",
        )

    def create(self, validated_data):
        category = validated_data.pop("category")
        instance, created = PublicIconsCategory.objects.get_or_create(**category)
        Community = PublicIcons.objects.create(**validated_data, category=instance)

        return Community

    def update(self, instance, validated_data):
        if "category" in validated_data:
            nested_serializer = self.fields["category"]
            nested_instance = instance.category
            nested_data = validated_data.pop("category")
            nested_serializer.update(nested_instance, nested_data)

        return super(PublicIconsWriteSerializer, self).update(instance, validated_data)


class UserProfileDataSerializer(serializers.ModelSerializer):
    """
    Serializer class for User Profile Data
    """

    class Meta:
        model = UserProfileData
        fields = "__all__"