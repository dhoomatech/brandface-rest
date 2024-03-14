from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_countries.fields import CountryField
import logging

from core.models import Location

class SOCIAL_AUTH_PLATFORM(models.TextChoices):
    NONE = 'NONE', _('NONE')
    GOOGLE = 'GOOGLE', _('GOOGLE')

class FILE_TYPES(models.TextChoices):
    NONE = 'NONE', _('NONE')
    IMAGE = 'IMAGE', _('IMAGE')
    PDF = 'PDF', _('PDF')
    DOC = 'DOC', _('DOC')
    VIDEO = 'VIDEO', _('VIDEO')


def upload_profile_picture(instance, filename):
    return "profile/{user}/{filename}".format(user=instance.user, filename=filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
            Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_verified', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False) # Super Admin User
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=100, null=True)
    email_code = models.CharField(max_length=100, null=True)
    social_auth = models.CharField(max_length=20,choices=SOCIAL_AUTH_PLATFORM.choices, default=SOCIAL_AUTH_PLATFORM.NONE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    REQUIRED_FIELDS = ['location', 'contact_number']


    def __str__(self):
        return f"{self.username} {self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfileData(models.Model):
    about = models.TextField(default='')
    website = models.CharField(max_length=255, null=False,default='',blank=True)
    description = models.CharField(max_length=255, null=False,default='')
    referal_code = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False) # Admin User
    is_ass_admin = models.BooleanField(default=False) # Associated Admin User
    date_of_birth = models.DateField(null=True)
    avatar = models.ImageField(upload_to=upload_profile_picture, blank=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.user.email}"

    @property
    def owner(self):
        return self.user

def upload_files(instance, filename):
    return "fileuploads/{user}/{filename}".format(user=instance.user, filename=filename)

class UserUploads(models.Model):
    class Meta:
        db_table = 'user_uploads'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to=upload_files, blank=True, null=False)
    created  = models.DateTimeField(default=timezone.now)
    file_type = models.CharField(max_length=20,choices=FILE_TYPES.choices, default=FILE_TYPES.NONE)


class Address(models.Model):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    longitude = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
    

def public_icon_image_path(instance, filename):
    return f"pulicicon/images/{instance.name}/{filename}"


class PublicIconsCategory(models.Model):
    name = models.CharField(_("Category name"), max_length=100)
    icon = models.ImageField(upload_to=public_icon_image_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Community Category")
        verbose_name_plural = _("Community Categories")

    def __str__(self):
        return self.name

class PublicIcons(models.Model):
    category = models.ForeignKey(PublicIconsCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
