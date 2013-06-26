from logging import getLogger
logger = getLogger('telemetry_requests')
from .models import add_request, log_request


class RecordRequestMiddleware(object):
    def process_request(self, request):
        log_request(request)
        try:
            add_request(request)
        except Exception, error:
            print "the error was: %s" % error
        return None
