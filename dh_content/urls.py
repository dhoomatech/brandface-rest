from django.shortcuts import render
from rest_framework import routers
from dh_content.views import *
from django.urls import include, path

# Create your views here.
from django.urls import path

from . import views
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(f"profile", ProfileLinksViewSet)
# router.register("profile", ProfileLinkViewSet)
router.register(r'profile2', ProfileLinkViewSet2, basename='profilelinks')
router.register(r'social', SocialMediaViewSet, basename='profisociallelinks')
router.register(r'user-connct', UserConnectionsViewSet, basename='user-connct')
router.register(r'user-gallary', UserGalleryViewSet, basename='user-gallary')
router.register(r'user-services', UserServicesViewSet, basename='user-services')

urlpatterns = [
        
]