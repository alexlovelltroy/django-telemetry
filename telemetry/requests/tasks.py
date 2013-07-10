from .models import tx_add_request
try:
    from celery.task import task
except ImportError:
    from celery.decorators import task


@task
def record_request(path=None,
                   user=None,
                   http_user_agent=None,
                   http_referer=None,
                   remote_addr=None,
                   server_name=None,
                   timestamp=None):
    tx_add_request(path = path,
                   user = user,
                   http_user_agent = http_user_agent,
                   http_referer = http_referer,
                   remote_addr = remote_addr,
                   server_name = server_name,
                   timestamp = timestamp)

