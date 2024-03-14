from django.contrib import admin
from dh_user.models import Address,UserProfileData,UserUploads

# Register your models here.


admin.site.register(UserProfileData)
admin.site.register(UserUploads)
admin.site.register(Address)
