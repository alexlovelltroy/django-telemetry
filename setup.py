from distutils.core import setup
import os


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('telemetry'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath
        for f in filenames:
            data_files.append(os.path.join(prefix, f))
print data_files

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
    include_package_data=True,
    package_data = { 'telemetry.reporting': [
        "static/javascripts/*.js",
        "static/*.css",
        "templates/*.html",
    ]},
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
