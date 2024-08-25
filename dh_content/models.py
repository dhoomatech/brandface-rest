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
    username = models.CharField(max_length=255, unique=True, null=False,default='',blank=True)
    tittle = models.CharField(max_length=255)
    about = models.TextField(default='')
    website = models.CharField(max_length=255, default='', null=False,blank=True)
    email = models.CharField(max_length=255, default='', null=False,blank=True)
    phone_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=False,default='')
    avatar = models.ImageField(upload_to=upload_profile_avatar, blank=True, null=False)
    background = models.ImageField(upload_to=upload_profile_background, blank=True, null=False)
    background_color = models.CharField(max_length=50, default='', null=False,blank=True)
    qr_file = models.FileField(upload_to="qr-code", blank=True, null=False)
    status = models.BooleanField(default=1)
    
    def __str__(obj):
        return str(obj.username)
    
    def save(self, *args, **kwargs):
        self.qr_generator(self, *args, **kwargs)
        if not self.username:
            username = self.tittle
            phone_number = str(self.phone_number)
            username = username.replace(" ", "-")
            phone_number = phone_number.replace("+", "")
            self.username = f'{username}-{phone_number}'
        return super().save(*args, **kwargs)

    def qr_generator(self, *args, **kwargs):
        try:
            
            import string
            import random
            import qrcode
            import os

            img_dir = os.path.join(settings.MEDIA_ROOT, 'qrcode')
            os.makedirs(img_dir, exist_ok=True) 
            
            unic_code = f'{self.username}.{settings.SITE_HOST}'
            unic_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            
            img = qrcode.make(unic_code)

            img_name = f'{unic_name}.png'
            img_path = os.path.join(img_dir, img_name)
            img.save(img_path)

            self.qr_file = os.path.relpath(img_path, settings.MEDIA_ROOT)
            # self.save()


        except Exception as e:
            import traceback
            traceback.print_exc()


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