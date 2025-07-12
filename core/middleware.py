import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from rest_framework import status
from django.conf import settings
from subscriptions.models import Subscription

class RateLimitMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.method == 'POST' and request.path.startswith('/chatroom'):
            try:
                subscription = request.user.subscription
                if subscription.tier == 'pro':
                    return None
            except Subscription.DoesNotExist:
                pass
            key = f"prompt_count_{request.user.id}_{request.user.subscription.start_date.date() if hasattr(request.user, 'subscription') and request.user.subscription.start_date else ''}"
            count = cache.get(key, 0)
            if count >= 5:
                return JsonResponse({'error': 'Daily prompt limit reached for Basic users.'}, status=429)
            cache.incr(key)
            cache.expire(key, 86400)  # 1 day
        return None

class GlobalExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        return JsonResponse({'error': str(exception)}, status=500)

def custom_exception_handler(exc, context):
    """Custom exception handler for DRF"""
    from rest_framework.views import exception_handler
    from rest_framework.response import Response
    
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response 