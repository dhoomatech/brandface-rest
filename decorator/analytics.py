import re
from functools import wraps
from django.utils.timezone import now
from cards.models import BusinessProfile
from analytics.models import ProfileVisit

def track_profile_visit(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        unique_name = kwargs.get('slug')
        if unique_name:
            try:
                profile = BusinessProfile.objects.get(unique_name=unique_name)
                ip = get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                ProfileVisit.objects.using('analytics').create(
                    profile=profile,
                    ip_address=ip,
                    user_agent=user_agent,
                    visited_at=now()
                )
            except BusinessProfile.DoesNotExist:
                pass  # Invalid profile, skip logging

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
