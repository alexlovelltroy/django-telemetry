from django.db import models
from django.conf import settings

class Event(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    recorded_time = models.DateTimeField(auto_now_add=True)
    when = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    action = models.CharField(max_length=64, blank=True, null=True)
    label = models.CharField(max_length=64, blank=True, null=True)
    what = models.CharField(max_length=255, blank=True, null=True)


