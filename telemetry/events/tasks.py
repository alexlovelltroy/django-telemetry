#import logging
#logger = logging.getLogger(__name__)
from .models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

@task
def add_metric( who=None,
                when=None,
                what=None,
                category=None,
                action=None,
                label=None
               ):
        if who:
            #assume it's an e-mail
            try:
                user = User.objects.get(email=who)
            except User.DoesNotExist:
                user = None
        else:
            user = None
        obj = Event(
            who = user,
            when = when,
            what = unicode(what),
            category = unicode(category),
            action = unicode(action),
            label = unicode(label),
        )
        #logger.debug("prepared to record a metric %s " % what)
        obj.save()
