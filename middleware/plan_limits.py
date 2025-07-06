from django.http import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from cards.models import BusinessProfile, Service, GalleryImage, SocialMedia
from utils.plans import USER_PLAN_LIMITS
import re

class PlanLimitMiddleware:
    """
    Middleware to restrict adding services, gallery images, and social links
    based on the user's subscription plan.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        self.url_config = {
            'services': {
                'pattern': r'/api/cards/services/?$',
                'model': Service,
                'related_name': 'services'
            },
            'gallery': {
                'pattern': r'/api/cards/gallery/?$',
                'model': GalleryImage,
                'related_name': 'gallery'
            },
            'social_links': {
                'pattern': r'/api/cards/social/?$',
                'model': SocialMedia,
                'related_name': 'social_links'
            },
        }

    def __call__(self, request):
        # Restrict only POST requests
        if request.method == "POST" and request.user.is_authenticated:
            for key, config in self.url_config.items():
                if re.match(config['pattern'], request.path):
                    return self._check_limit(request, key, config)
        return self.get_response(request)

    def _check_limit(self, request, key, config):
        user = request.user
        plan = getattr(user, 'plan', 'free')
        profile_id = request.POST.get('profile') or request.data.get('profile')

        if not profile_id:
            return JsonResponse({"detail": "Business profile is required."}, status=HTTP_403_FORBIDDEN)

        try:
            profile = BusinessProfile.objects.get(id=profile_id, owner=user)
        except BusinessProfile.DoesNotExist:
            return JsonResponse({"detail": "Profile not found or not owned by you."}, status=HTTP_403_FORBIDDEN)

        current_count = getattr(profile, config['related_name']).count()
        allowed = USER_PLAN_LIMITS[plan].get(key, 0)

        if current_count >= allowed:
            return JsonResponse({
                "status": "failed",
                "message": f"Your current plan '{plan}' allows only {allowed} {key.replace('_', ' ')}."
            }, status=HTTP_403_FORBIDDEN)

        return self.get_response(request)
