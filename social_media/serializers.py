# reviews/serializers.py
from rest_framework import serializers

class InstagramPostSerializer(serializers.Serializer):
    id = serializers.CharField()
    caption = serializers.CharField(required=False)
    media_url = serializers.URLField()
    permalink = serializers.URLField()
    timestamp = serializers.DateTimeField()
