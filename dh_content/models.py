from django.db import models
# from phone_field import PhoneField
from django.utils import timezone
from django.conf import settings
# Create your models here.
from dh_user.models import User



def upload_profile_avatar(instance, filename):
    return "profile/avatar/".format(user=instance.ProfileLinks, filename=filename)

def upload_profile_background(instance, filename):
    return "profile/background/".format(user=instance.ProfileLinks, filename=filename)

class ProfileLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False,default='',blank=True)
    about = models.TextField(default='')
    website = models.CharField(max_length=255, default='', null=False,blank=True)
    description = models.CharField(max_length=255, null=False,default='')
    avatar = models.ImageField(upload_to=upload_profile_avatar, blank=True, null=False)
    background = models.ImageField(upload_to=upload_profile_background, blank=True, null=False)
    background_color = models.CharField(max_length=50, default='', null=False,blank=True)

    def __str__(obj):
        return str(obj.username)


class SocialMedia(models.Model):
    name = models.CharField(max_length = 250, null=False)
    created  = models.DateTimeField(default=timezone.now)
    icon = models.FileField(upload_to="icon-images", null=False,default='')
    status = models.BooleanField(default=1)

    def __str__(obj):
        return str(obj.name)
    

class UserConnections(models.Model):
    profile = models.ForeignKey(ProfileLinks, on_delete=models.CASCADE,null=False,blank=True)
    social = models.ForeignKey(SocialMedia, on_delete=models.CASCADE,null=False,blank=True)
    value = models.TextField(default='')
    status = models.BooleanField(default=1)


class UserGallery(models.Model):
    profile = models.ForeignKey(ProfileLinks, on_delete=models.CASCADE,null=False,blank=True)
    picture = models.FileField(upload_to="profile-images", null=False,default='')
    created  = models.DateTimeField(default=timezone.now)
    
class UserServices(models.Model):
    profile = models.ForeignKey(ProfileLinks, on_delete=models.CASCADE,null=False,blank=True)
    tittle = models.TextField(default='')
    description = models.TextField(default='')
    picture = models.FileField(upload_to="profile-images", null=False,default='')
    created  = models.DateTimeField(default=timezone.now)