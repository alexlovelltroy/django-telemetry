from .tasks import record_request
import datetime
from pytz import utc

class RecordRequestMiddleware(object):
    def process_template_response(self, request, response):
        if response.status_code == 200:
            try:
                # grab things from the request object
                record_request.delay(
                    path = request.path,
                    user = request.user,
                    http_user_agent = request.META.get('HTTP_USER_AGENT'),
                    http_referer = request.META.get('HTTP_REFERER'),
                    remote_addr = request.META.get('REMOTE_ADDR'),
                    server_name = request.META.get('SERVER_NAME'),
                    timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
                )
            except Exception:
                pass
        return response
