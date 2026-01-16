from django.contrib import admin
from .models import RequestLog, BlockedIP
# Register your models here.

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp')
    list_filter = ('ip_address',)
    search_fields = ('ip_address', 'path')
    ordering = ('-timestamp',)


