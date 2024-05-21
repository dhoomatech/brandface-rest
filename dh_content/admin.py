from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserConnections)

class AdminSocialMedia(admin.ModelAdmin):
    list_display = ['id','name' ,'icon','status']

admin.site.register(SocialMedia,AdminSocialMedia)


class UserGalleryMedia(admin.ModelAdmin):
    list_display = ['id','profile','picture']

admin.site.register(UserGallery,UserGalleryMedia)


class UserServicesMedia(admin.ModelAdmin):
    list_display = ['id','profile','picture','tittle']

admin.site.register(UserServices,UserServicesMedia)