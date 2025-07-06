from django.urls import path
from .views import InstagramPostAPIView

urlpatterns = [
    path('instagram-posts/<slug:unique_name>/', InstagramPostAPIView.as_view(), name='instagram-posts'),
]
