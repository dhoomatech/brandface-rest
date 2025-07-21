import re
from django.utils.timezone import now
from cards.models import BusinessProfile
from analytics.models import ProfileVisit


class TrackProfileVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.visit_url_pattern = re.compile(r'^/cards/api/v1/profiles-data/public/(?P<slug>[\w-]+)/?$')

    def __call__(self, request):
        match = self.visit_url_pattern.match(request.path)

        if match:
            unique_name = match.group('slug')
            try:
                profile = BusinessProfile.objects.get(unique_name=unique_name)

                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Save to analytics database
                ProfileVisit.objects.using('analytics').create(
                    profile=profile,
                    ip_address=ip,
                    user_agent=user_agent,
                    visited_at=now()
                )

            except BusinessProfile.DoesNotExist:
                pass  # skip if not a valid profile

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

