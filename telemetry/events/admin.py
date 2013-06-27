from django.contrib import admin

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = (
                    'recorded_time',
                    'who',
                    'category',
                    'action',
                    'label',
                    'what',
                    'when',
    )

admin.site.register(Event, EventAdmin)
