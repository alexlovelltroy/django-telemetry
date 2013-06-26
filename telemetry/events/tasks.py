import logging
logger = logging.getLogger(__name__)
from .models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

@task
def metric_task(**kwargs):
    if 'who' in kwargs:
        #assume it's an e-mail
        try:
            user = User.objects.get(email=kwargs['who'])
        except User.DoesNotExist:
            user = None
        kwargs.update(who=user)
    logger.debug("prepared to record a metric %s " % kwargs)
    Event.objects.create(kwargs)
