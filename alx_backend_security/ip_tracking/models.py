from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()  # stores IPv4 or IPv6
    timestamp = models.DateTimeField(auto_now_add=True)  # automatically sets when request is logged
    path = models.CharField(max_length=255)  # URL path the user accessed

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"
