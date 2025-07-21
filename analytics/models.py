from django.db import models

# Create your models here.



class ProfileVisit(models.Model):
    profile = models.ForeignKey('cards.BusinessProfile', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.business_name} visited at {self.visited_at}"
