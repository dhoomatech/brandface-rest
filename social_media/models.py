from django.db import models
from cards.models import BusinessProfile

# Create your models here.

class SocialMediaConfig(models.Model):
    profile = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='google_config')
    google_api_key = models.CharField(max_length=255)  # Store securely if sensitive

    def __str__(self):
        return f"Social media Config for {self.profile.business_name}"


class GoogleReview(models.Model):
    profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='google_reviews')
    author_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    text = models.TextField(blank=True)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.author_name} ({self.rating})"


class InstagramConfig(models.Model):
    profile = models.OneToOneField(BusinessProfile, on_delete=models.CASCADE, related_name='instagram_config')
    instagram_user_id = models.CharField(max_length=100)
    access_token = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)