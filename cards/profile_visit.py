from django.core.cache import cache
from django.http import JsonResponse
from .models import BusinessProfile

def track_visit(request, uuid):
    cache_key = f"profile_visit_count:{uuid}"
    visit_count = cache.get(cache_key, 0)
    visit_count += 1
    cache.set(cache_key, visit_count, timeout=86400)  # 1 day

    # Optional: retrieve profile
    profile = BusinessProfile.objects.filter(uuid=uuid).first()
    return JsonResponse({
        "profile": profile.name if profile else None,
        "visits": visit_count
    })
