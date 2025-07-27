import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.timezone import now

# Logging Middleware
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)
        return self.get_response(request)


# Time Restriction Middleware
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_block = datetime.strptime("21:00", "%H:%M").time()
        end_block = datetime.strptime("06:00", "%H:%M").time()

        if current_time >= start_block or current_time < end_block:
            return HttpResponseForbidden("Access to the chat is restricted between 9PM and 6AM.")

        return self.get_response(request)


# Rate Limit Middleware
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # key: ip, value: list of datetime objects

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now_time = now()

        if request.method == 'POST' and '/chats/' in request.path:
            self.cleanup_old_requests(ip, now_time)
            self.requests.setdefault(ip, []).append(now_time)

            if len(self.requests[ip]) > 5:
                return HttpResponseForbidden("Rate limit exceeded: Maximum 5 messages per minute allowed.")

        return self.get_response(request)

    def cleanup_old_requests(self, ip, current_time):
        one_minute_ago = current_time - timedelta(minutes=1)
        self.requests[ip] = [timestamp for timestamp in self.requests.get(ip, []) if timestamp > one_minute_ago]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
