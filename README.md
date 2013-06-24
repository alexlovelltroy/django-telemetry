# django-telemetry
## Record and Store all your own data

There are many external analytics packages that can tell you about your users in aggregate.  We like [Google Analytics](http://google.com/analytics) for that.  To store information about requests along with the users who made them, we like django-telemetry.

### Async operation with celery

If you are running a celery task queue, recording of the views in the database can be separated from the actual request.

### Middleware vs Decorator vs Mixin

Depending on your performance needs, telemetry can be recorded at different points in the request/response cycle.  Middleware plays nicely with most kinds of caching and is easiest to set up.  You probably want that.

If you really want to exert more control, the Mixin and Decorator are provided
