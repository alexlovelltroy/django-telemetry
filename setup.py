from distutils.core import setup

setup(
    name='django-telemetry',
    version='0.1.0',
    author='Alex Lovell-Troy',
    author_email='alex@lovelltroy.org',
    description='Event-based reporting system for django - with queryset graphs',
    packages=[
        'telemetry',
        'telemetry.events',
        'telemetry.events.migrations',
        'telemetry.metrics',
        'telemetry.reporting',
        'telemetry.requests',
    ],
    url='https://github.com/alexlovelltroy/django-telemetry',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.5",
        "pytz >= 2013.9",
        "django-celery >= 3.1",
        "South >= 0.8",
    ],
)
