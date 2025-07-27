import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_block = time(21, 0)  # 9 PM
        end_block = time(6, 0)     # 6 AM

        # If current time is between 9PM and 6AM, deny access
        if current_time >= start_block or current_time < end_block:
            return HttpResponseForbidden("Access to the chat is restricted between 9PM and 6AM.")

        return self.get_response(request)
