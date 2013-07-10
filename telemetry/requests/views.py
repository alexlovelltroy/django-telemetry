# Create your views here.
from .tasks import record_request
import datetime
from pytz import utc

def LogRequestMixin(object):
    def dispatch(self, request, *args, **kwargs):
        record_request.delay(
            path = request.path,
            user = request.user,
            http_user_agent = request.META.get('HTTP_USER_AGENT'),
            http_referer = request.META.get('HTTP_REFERER'),
            remote_addr = request.META.get('REMOTE_ADDR'),
            server_name = request.META.get('SERVER_NAME'),
            timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
        )
        return super(LogRequestMixin, self).dispatch(request, *args, **kwargs)
