from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP
import logging

logger = logging.getLogger(__name__)

@shared_task
def detect_anomalous_ips():
    """
    Celery task to detect anomalous IP addresses based on:
    1. More than 100 requests per hour
    2. Accessing sensitive paths like /admin, /login
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    sensitive_paths = ['/admin', '/login', '/api/admin', '/admin/', '/login/', '/api/login']
    
    # Find IPs with more than 100 requests in the last hour
    high_volume_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('id')
    ).filter(request_count__gt=100)
    
    for entry in high_volume_ips:
        ip_address = entry['ip_address']
        request_count = entry['request_count']
        reason = f"High volume: {request_count} requests in the last hour"
        
        SuspiciousIP.objects.get_or_create(ip_address=ip_address, defaults={'reason': reason})
        logger.info(f"Flagged IP {ip_address} for high volume: {request_count} requests")
    
    # Find IPs accessing sensitive paths (combines both checks in one query)
    sensitive_access = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address', 'path').annotate(
        access_count=Count('id')
    )
    
    for entry in sensitive_access:
        ip_address = entry['ip_address']
        path = entry['path']
        access_count = entry['access_count']
        
        if access_count > 5:
            reason = f"Frequent access to sensitive path '{path}': {access_count} times"
        else:
            reason = "Accessed sensitive path"
        
        SuspiciousIP.objects.get_or_create(ip_address=ip_address, defaults={'reason': reason})
        logger.info(f"Flagged IP {ip_address}: {reason}")