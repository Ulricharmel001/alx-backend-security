from .models import RequestLog, BlockedIP
from ipware import get_client_ip  
import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden
import os
from dotenv import load_dotenv
load_dotenv()

class IPLoggingMiddleware:
    """
    Middleware to log IP, timestamp, and path for each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = None 
        path = request.path

        # Get country and city
        geo = get_geo_data(ip) if ip else {"country": None, "city": None}

        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            country=geo["country"],
            city=geo["city"],
        )

        response = self.get_response(request)
        return response


# Middleware to log requests and block blacklisted IPs
class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip is None:
            ip = None
        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")
        response = self.get_response(request)
        return response


CACHE_TIMEOUT = 60 * 60 * 24
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")   

def get_geo_data(ip):
    cache_key = f"geo_{ip}"
    geo_data = cache.get(cache_key)
    if geo_data:
        return geo_data

    try:
        res = requests.get(
            f"https://ipinfo.io/{ip}/json",
            headers={"Authorization": f"Bearer {IPINFO_TOKEN}"},
            timeout=3
        )
        if res.status_code == 200:
            data = res.json()
            geo_data = {
                "country": data.get("country"),
                "city": data.get("city"),
            }
            cache.set(cache_key, geo_data, CACHE_TIMEOUT)
            return geo_data
    except requests.RequestException:
        pass

    return {"country": None, "city": None}
