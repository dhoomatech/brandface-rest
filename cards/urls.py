from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessProfileViewSet, SocialMediaViewSet, ServiceViewSet, GalleryImageViewSet

router = DefaultRouter()
router.register('profiles', BusinessProfileViewSet, basename='profiles')
router.register('social', SocialMediaViewSet, basename='social')
router.register('services', ServiceViewSet, basename='services')
router.register('gallery', GalleryImageViewSet, basename='gallery')


urlpatterns = [
    path('', include(router.urls)),
]
