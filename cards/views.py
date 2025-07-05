from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from .models import BusinessProfile, SocialMedia, Service, GalleryImage
from .serializers import (
    BusinessProfileSerializer, SocialMediaSerializer,
    ServiceSerializer, GalleryImageSerializer
)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        name = request.query_params.get('name')
        profile = get_object_or_404(BusinessProfile, unique_name=name)
        serializer = BusinessProfileSerializer(profile)
        return Response(serializer.data)


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SocialMedia.objects.filter(profile__owner=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(BusinessProfile, id=self.request.data.get('profile'))
        if profile.owner != self.request.user:
            raise PermissionDenied("Not allowed to add links to this profile.")
        serializer.save(profile=profile)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(profile__owner=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(BusinessProfile, id=self.request.data.get('profile'))
        if profile.owner != self.request.user:
            raise PermissionDenied("Not allowed to add services to this profile.")
        serializer.save(profile=profile)


class GalleryImageViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GalleryImage.objects.filter(profile__owner=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(BusinessProfile, id=self.request.data.get('profile'))
        if profile.owner != self.request.user:
            raise PermissionDenied("Not allowed to add gallery images to this profile.")
        serializer.save(profile=profile)

