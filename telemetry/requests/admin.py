import logging
logger = logging.getLogger(__name__)
from django.contrib import admin
from .models import (
    Request,
    UserAgent,
    HttpReferer
)

class HttpRefererAdmin(admin.ModelAdmin):
    list_display = ('http_referer', 'first_seen')

class UserAgentAdmin(admin.ModelAdmin):
    list_display = ('http_user_agent', 'first_seen', 'is_spider')

class RequestAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'path', 'remote_addr', 'user')

admin.site.register(Request, RequestAdmin)
admin.site.register(UserAgent, UserAgentAdmin)
admin.site.register(HttpReferer, HttpRefererAdmin)
