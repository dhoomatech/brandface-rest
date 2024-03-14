from django.db import models
# from phone_field import PhoneField
from django.utils import timezone
from django.conf import settings
# Create your models here.
from dh_user.models import User


class SocialMedia(models.Model):
    name = models.CharField(max_length = 250, null=False)
    created  = models.DateTimeField(default=timezone.now)
    icon = models.FileField(upload_to="icon-images", null=False,default='')
    status = models.BooleanField(default=1)

    def __str__(obj):
        return str(obj.name)
    

class UserConnections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    value = models.TextField(default='')
    status = models.BooleanField(default=1)


class UserGallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to="profile-images", null=False,default='')
    created  = models.DateTimeField(default=timezone.now)
    
class UserServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tittle = models.TextField(default='')
    description = models.TextField(default='')
    picture = models.FileField(upload_to="profile-images", null=False,default='')
    created  = models.DateTimeField(default=timezone.now)