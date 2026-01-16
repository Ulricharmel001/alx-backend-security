
from .models import RequestLog
from ipware import get_client_ip  

class IPLoggingMiddleware:
    """
    Middleware to log IP, timestamp, and path for each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0" 
        path = request.path
        RequestLog.objects.create(ip_address=ip, path=path) 
        response = self.get_response(request)
        return response


# Middleware to log requests and block blacklisted IPs
class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0" 
        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")
        response = self.get_response(request)
        return response
