from django.urls import path
from . import views

urlpatterns = [
    path('OIP/public/ping', views.ping_view, name='ping'),
]
