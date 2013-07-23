from django.db import models
from django.conf import settings

class Metric(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    count = models.IntegerField()

    def increment(self):
        self.count = self.count + 1

class DayMetric(Metric):
    when = models.DateField(null=True, blank=True)

class WeekMetric(Metric):
    when = models.DateField(null=True, blank=True)

class MonthMetric(Metric):
    when = models.DateField(null=True, blank=True)
