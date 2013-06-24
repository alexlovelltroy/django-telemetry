from .models import add_request


class RecordRequestMiddleware(object):
    def process_request(self, request):
        try:
            add_request(request)
        except:
            pass
