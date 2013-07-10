from logging import getLogger
logger = getLogger('telemetry_requests')
import datetime
from django.utils.timezone import utc
from django.db import models, transaction
from django.conf import settings

# Create your models here.

class UserAgent(models.Model):
    http_user_agent = models.CharField(max_length=255, unique=True)
    is_spider = models.BooleanField(default=False)
    first_seen = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.http_user_agent[:20]

    @property
    def request_count(self):
        return len(self.requests_set.all())


class HttpReferer(models.Model):
    http_referer = models.URLField(max_length=255, unique=True)
    first_seen = models.DateTimeField(auto_now_add=True)

    @property
    def request_count(self):
        return len(self.requests_set.all())

    def __unicode__(self):
        return self.http_referer[:20]



class LiveRequestManager(models.Manager):
    def get_queryset(self):
        return super(LiveRequestManager, self).get_queryset().filter(http_referer__is_spider=False)


class SpiderRequestManager(models.Manager):
    def get_queryset(self):
        return super(SpiderRequestManager, self).get_queryset().filter(http_referer__is_spider=True)


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None)
    http_user_agent = models.ForeignKey(UserAgent, null=True, default=None)
    http_referer = models.ForeignKey(HttpReferer, null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=256)
    remote_addr = models.CharField(max_length=256)
    server_name = models.CharField(max_length=256)
    by_people = LiveRequestManager()
    by_spider = SpiderRequestManager()


def add_request(request):
    # grab things from the request object
    tx_add_request(
        path = request.path,
        user = request.user,
        http_user_agent = request.META.get('HTTP_USER_AGENT'),
        http_referer = request.META.get('HTTP_REFERER'),
        remote_addr = request.META.get('REMOTE_ADDR'),
        server_name = request.META.get('SERVER_NAME'),
        timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
    )



@transaction.commit_on_success
def tx_add_request(path=None,
                   user=None,
                   http_user_agent=None,
                   http_referer=None,
                   remote_addr=None,
                   server_name=None,
                   timestamp=None):
    """Made to be run within a transaction so that it all succeeds or fails together """
    if not path:
        return None
    if http_user_agent:
        normalized = http_user_agent.strip()[:255]
        useragent, created = UserAgent.objects.get_or_create(http_user_agent=normalized)
    else:
        useragent = None
    if  http_referer:
        normalized = http_referer.strip()[:255]
        referer, created = HttpReferer.objects.get_or_create(http_referer=normalized)
    else:
        referer = None


    create_dict = dict(
        http_user_agent = useragent,
        http_referer = referer,
        path = path
    )
    if user:
        if user.is_authenticated():
            create_dict.update(user = user)

    if remote_addr:
        create_dict.update(dict(
            remote_addr = remote_addr
        ))
    if server_name:
        create_dict.update(dict(
            server_name = server_name
        ))
    if timestamp:
        create_dict.update(dict(
            timestamp = timestamp
        ))
    request_obj =  Request(**create_dict)
    request_obj.save()


def log_request(request):
    if request.user.is_authenticated():
        logger.info('%s viewed %s' % (request.user.email, request.path))

