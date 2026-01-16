
from .models import RequestLog
from ipware import get_client_ip  # helps get correct client IP even behind proxies

class IPLoggingMiddleware:
    """
    Middleware to log IP, timestamp, and path for each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client IP
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0" #fall back here
        path = request.path
        RequestLog.objects.create(ip_address=ip, path=path) #create log entry
        response = self.get_response(request)
        return response
