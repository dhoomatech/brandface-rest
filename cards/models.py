from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BusinessProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_cards')
    unique_name = models.SlugField(unique=True)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField(upload_to='social_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform} - {self.profile.business_name}"


class Service(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    # Optional: image upload
    image = models.ImageField(upload_to='service/', blank=True, null=True)

    # Optional: use an icon name (e.g., "fa-solid fa-user")
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome or similar icon class")

    description = models.TextField()

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.profile.business_name}"
