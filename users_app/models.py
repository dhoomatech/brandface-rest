from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.tokens import default_token_generator

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('free_user', 'Free User'),
        ('basic_user', 'Basic User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class BlacklistedAccessToken(models.Model):
    token_jti = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
