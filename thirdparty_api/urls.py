from django.urls import path
from .views import KeywordSuggestionAPIView

urlpatterns = [
    path('keyword-suggestions/', KeywordSuggestionAPIView.as_view(), name='keyword-suggestions'),
]
