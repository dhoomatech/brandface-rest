from django.db import models
from cards.models import BusinessProfile  # Adjust this import based on your app

class Enquiry(models.Model):
    business_card = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="enquiries")
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
