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
from rest_framework.views import APIView
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
    permission_classes = [IsUserProfileOwner,]
    http_method_names = ['post']

    def create(self, request, pk=None):
        user = request.user
        request_data = request.data
        super().create(self, request, pk=None)

        return Response({'status': 'password set'})
        
class ProfileLinkViewSet2(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = ProfileLinks.objects.all()
    serializer_class = ProfileLinksCreateSerializer
    permission_classes = [IsUserProfileOwner,]

    def create(self, request):
        try:
            user = request.user
            request_post = request.POST
            # print(request_post)
            serializer = ProfileLinkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                save_data = serializer.data
                return Response({'msg':'Data  created','data':save_data}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'msg':str(e), 'status':"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserNameCheck(APIView):
    def get(self, request,user_name):
        
        if ProfileLinks.objects.filter(username=user_name).exists():
            return Response({'msg':'Already Exist','validation':False}, status=status.HTTP_302_FOUND)
        else:
            return Response({'msg':'User Name Available','validation':True}, status=status.HTTP_201_CREATED)


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
    permission_classes = [permissions.AllowAny,]
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
    # http_method_names = ['post']

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


class ProfileDataGet(APIView):
    def get(self, request,user_name):

        user_profile_obj = ProfileLinks.objects.filter(username=user_name,status=True).first()
        if user_profile_obj:
            serializer_data = ProfileReadSerializer(user_profile_obj)
            return Response({'msg':'User profile data','data':serializer_data.data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'User profile data not availabe','data':[]}, status=status.HTTP_404_NOT_FOUND)
        


# from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
class FileUploadView(APIView):
    # queryset = UserGallery.objects.all()
    serializer_class = UserGallerySerializer
    permission_classes = (IsUserProfileOwner,)
    # parser_classes = (FileUploadParser,)
    def post(self, request):
        serializer = UserGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'File uploaded successfully','data':serializer.data})
        else:
            return Response(serializer.errors, status=400)