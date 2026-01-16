from django.db import models
# log request ip to db 
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()  
    timestamp = models.DateTimeField(auto_now_add=True) 
    path = models.CharField(max_length=255)  
    city = models.CharField(max_length=225, null=True)
    country = models.CharField(max_length=225, null=True)
    

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

# This model track ip address which are blacklisted 
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    def __str__(self):
        return self.ip_address
