from django.views.generic import TemplateView
from .utils import build_report
import datetime
import time
#TODO change this to the pluggable user models
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class UserGraphView(TemplateView):
    template_name = "telemetry/usergraph.html"
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        report = build_report([
            dict(obj=User,date_field='date_joined',label="Users"),
        ], average=True)
        # This is naive and only serves as an example
        dthandler = lambda obj: time.mktime(obj.timetuple()) if isinstance(obj, datetime.date) else None
        context.update({'totals_json': json.dumps(report, default=dthandler), })
        for key, value in report.iteritems():
            context.update({key: value})
        return context
