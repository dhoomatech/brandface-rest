from django.shortcuts import render
from django.views import View
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions


from dh_user.permissions import IsUserAddressOwner, IsUserProfileOwner
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


from rest_framework import permissions
from rest_framework import viewsets

from .serializer import *

# class ProfileLinkViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = ProfileLinks.objects.all()
#     serializer_class = ProfileLinksSerializer
#     # http_method_names = ['get', 'post', 'put']
#     http_method_names = []
    
#     def get_permissions(self):

#         if self.action == 'profile_create':
#             permission_classes = [permissions.IsAuthenticated]
#         if self.action == 'profile_update':
#             permission_classes = [permissions.IsAuthenticated]
#         if self.action == 'profile_read':
#             permission_classes = [permissions.IsAuthenticated]
#         elif self.action == 'profile_delete':
#             permission_classes = [permissions.IsAuthenticated]
#         else:
#             permission_classes = []
        
#         return [permission() for permission in permission_classes]

#     def get_serializer_class(self):
#             if self.action == 'profile_create':
#                 return ProfileLinksSerializer
#             elif self.action == 'profile_update':
#                 return ProfileLinksSerializer
#             # elif self.action == 'profile_read':
#             #     return ProfileLinksSerializer
#             # elif self.action == 'profile_delete':
#             #     return ProfileLinksSerializer
    
#     @action(methods=['post'], detail=False, url_path='profile-create')
#     def profile_create(self, request, *args, **kwargs):
#         print(request.user)
#         return Response({'status': True})

#     @action(methods=['put'], detail=True, url_path='profile-update')
#     def profile_update(self, request, *args, **kwargs):
#         print(request.user)
#         return Response({'status': True})

class ProfileLinkViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = ProfileLinks.objects.all()
    serializer_class = ProfileLinksSerializer
    permission_classes = (IsUserProfileOwner,)
    http_method_names = ['post']
    @action(detail=False, methods=['post'])
    def profile_create(self, request, pk=None):

        return Response({'status': 'password set'})
        
class ProfileLinkViewSet2(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = ProfileLinks.objects.all()
    serializer_class = ProfileLinksSerializer
    permission_classes = (IsUserProfileOwner,)

    def create(self, request):
        return Response({'status': 'password set'})

class ProfileLinksViewSet(ReadOnlyModelViewSet):
    queryset = ProfileLinks.objects.all()
    serializer_class = ProfileLinkReadSerializer
    permission_classes = (IsUserProfileOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)

class SocialMediaViewSet(ReadOnlyModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']

class UserConnectionsViewSet(ReadOnlyModelViewSet):
    queryset = UserConnections.objects.all()
    serializer_class = UserConnectionsSerializer
    permission_classes = (IsUserProfileOwner,)
    http_method_names = ['get','post','patch']

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(profile__user=user)


class UserGalleryViewSet(ReadOnlyModelViewSet):
    queryset = UserGallery.objects.all()
    serializer_class = UserGallerySerializer
    permission_classes = (IsUserProfileOwner,)
    http_method_names = ['get','post','patch']

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(profile__user=user)

class UserServicesViewSet(ReadOnlyModelViewSet):
    queryset = UserServices.objects.all()
    serializer_class = UserServicesSerializer
    permission_classes = (IsUserProfileOwner,)
    http_method_names = ['get','post','patch']

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(profile__user=user)