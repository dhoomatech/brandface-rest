from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessProfileViewSet, SocialMediaViewSet, ServiceViewSet, GalleryImageViewSet,BusinessProfileViewPublic, SocialMediaPlatformViewSet

# DRF imports for viewsets
from rest_framework.urlpatterns import format_suffix_patterns

business_profile_list = BusinessProfileViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
business_profile_detail = BusinessProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

business_profile_public = BusinessProfileViewPublic.as_view({
    'get': 'public'
})

social_list = SocialMediaViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
social_detail = SocialMediaViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

service_list = ServiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
service_detail = ServiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

gallery_list = GalleryImageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
gallery_detail = GalleryImageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Business Profiles
    path('profiles/', business_profile_list, name='profiles-list'),
    path('profiles/<int:pk>/', business_profile_detail, name='profiles-detail'),

    # Public Business Profile by name
    path('profiles-data/public/<str:unique_name>', business_profile_public, name='profiles-public'),

    # Social Media
    path('social/', social_list, name='social-list'),
    path('social/<int:pk>/', social_detail, name='social-detail'),
    path('social-platforms', SocialMediaPlatformViewSet.as_view({'get': 'list'}), name='social-platforms'),

    # Services
    path('services/', service_list, name='services-list'),
    path('services/<int:pk>/', service_detail, name='services-detail'),

    # Gallery
    path('gallery/', gallery_list, name='gallery-list'),
    path('gallery/<int:pk>/', gallery_detail, name='gallery-detail'),


]

urlpatterns = format_suffix_patterns(urlpatterns)