from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "Brandface"
admin.site.site_title = "Brandface Admin"
admin.site.index_title = "Welcome to Brandface Dashboard"

admin.site.register(User)