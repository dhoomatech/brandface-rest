from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied,NotFound 
from rest_framework.permissions import AllowAny

from .models import BusinessProfile, SocialMedia, Service, GalleryImage, SocialMediaPlatform
from .serializers import (
    BusinessProfileSerializer, SocialMediaSerializer,
    ServiceSerializer, GalleryImageSerializer, SocialMediaPlatformSerializer
)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class BusinessProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Business Profiles.
    - Authenticated users can create, view, update, and delete their profiles.
    - Public can access profile details via unique name using the `public` action.
    """
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    # encrypt_response = True  # Used by custom renderer for conditional encryption

    def get_queryset(self):
        """
        Return only the business profiles owned by the logged-in user.
        """
        user = self.request.user
        if not user.is_authenticated:
            return BusinessProfile.objects.none()
        return self.queryset.filter(owner=user)

    def perform_create(self, serializer):
        """
        Assign the logged-in user as the owner of the business profile on creation.
        """
        serializer.save(owner=self.request.user)


class BusinessProfileViewPublic(viewsets.ModelViewSet):
    """
    ViewSet for managing Business Profiles.
    - Authenticated users can create, view, update, and delete their profiles.
    - Public can access profile details via unique name using the `public` action.
    """
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='public/(?P<unique_name>[^/.]+)', permission_classes=[AllowAny])
    def public(self, request,version=None, unique_name=None):
        """
        Public endpoint to fetch a business profile by its unique_name.
        """
        if not unique_name:
            raise NotFound("Business unique name is required.")

        profile = get_object_or_404(BusinessProfile, unique_name=unique_name)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return SocialMedia.objects.none()
        return SocialMedia.objects.filter(profile__owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required.")

        profile_id = self.request.data.get('profile')
        if not profile_id:
            raise PermissionDenied("Profile ID is required.")

        profile = get_object_or_404(BusinessProfile, id=profile_id)

        if profile.owner != user:
            raise PermissionDenied("Not allowed to add links to this profile.")

        serializer.save(profile=profile)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Service.objects.none()
        return Service.objects.filter(profile__owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required.")

        profile_id = self.request.data.get('profile')
        if not profile_id:
            raise PermissionDenied("Profile ID is required.")

        profile = get_object_or_404(BusinessProfile, id=profile_id)

        if profile.owner != user:
            raise PermissionDenied("Not allowed to add services to this profile.")

        serializer.save(profile=profile)


class GalleryImageViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return GalleryImage.objects.none()
        return GalleryImage.objects.filter(profile__owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required.")

        profile_id = self.request.data.get('profile')
        if not profile_id:
            raise PermissionDenied("Profile ID is required.")

        profile = get_object_or_404(BusinessProfile, id=profile_id)

        if profile.owner != user:
            raise PermissionDenied("You do not own this business profile.")

        serializer.save(profile=profile)


class SocialMediaPlatformViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only
    queryset = SocialMediaPlatform.objects.all()
    serializer_class = SocialMediaPlatformSerializer
    permission_classes = [permissions.AllowAny]
