django-telemetry
================
An event-based reporting system for django -- With queryset graphs!

### Not fit for human consumption.  
This is a collection of event/reporting code that I've used in various places over the years.  It seems useful enough to share, but I haven't added docs or examples yet.


## Event Features
* Event reporting in middleware, decorators, and tasks
* Request recording using middleware, decorators, view Mixins.
* Organizing requests by user, referer, and browser signature where provided
* Optional async recording/reporting using celery

## Reporting Features
* Logs in the database with management commands to clear old logs
* Generic queryset graphs (using [flot](http://flotcharts.org) to track _any_ queryset with a date field

