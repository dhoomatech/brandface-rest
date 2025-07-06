from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from cards.models import BusinessProfile
from .models import GoogleReview
from .utils import fetch_google_reviews  # assuming utility is here
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.exceptions import NotFound
from .serializers import InstagramPostSerializer
from .utils import fetch_instagram_posts


class UpdateGoogleReviews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        profile = get_object_or_404(BusinessProfile, pk=pk, owner=request.user)

        reviews, error = fetch_google_reviews(profile)
        if error:
            return Response({"error": error}, status=400)

        GoogleReview.objects.filter(profile=profile).delete()

        for rev in reviews:
            GoogleReview.objects.create(
                profile=profile,
                author_name=rev.get("author_name", ""),
                rating=rev.get("rating", 0),
                text=rev.get("text", ""),
                time=datetime.fromtimestamp(rev.get("time", 0))
            )

        return Response({"status": "updated", "count": len(reviews)})



class InstagramPostAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, unique_name):
        profile = BusinessProfile.objects.filter(unique_name=unique_name).first()
        if not profile:
            raise NotFound("Business profile not found.")

        config = getattr(profile, 'instagram_config', None)
        if not config:
            raise NotFound("Instagram not configured for this profile.")

        posts = fetch_instagram_posts(config.instagram_user_id, config.access_token)
        serializer = InstagramPostSerializer(posts, many=True)
        return Response(serializer.data)