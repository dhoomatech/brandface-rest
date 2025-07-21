from django.core.cache import cache
from django.http import JsonResponse

class RedisRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith("/visit/"):
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate_limit:{ip}:{path}"
            hits = cache.get(key, 0)
            if hits >= 10:
                return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
            cache.set(key, hits + 1, timeout=60)  # 10 hits/minute

        return self.get_response(request)
