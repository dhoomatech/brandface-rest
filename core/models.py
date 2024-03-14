from django.db import models
from django_countries.fields import CountryField

# Create your models here.



class Location(models.Model):
    tittle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    user_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=100, blank=True)
    country = CountryField()
    longitude = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=100, blank=True)

# def get_default_location():
#     return Location.objects.get_or_create(tittle="kozhikode")[0]