from django.core.urlresolvers import reverse

from .models import RequestLog


class SaveRequestMiddleware(object):
    """
    Custom middleware for saving all http requests to database
    """
    def process_request(self, request):
        http_request = ' '.join(
            [request.META['REQUEST_METHOD'],
             request.META['PATH_INFO'],
             request.META['SERVER_PROTOCOL']]
        )
        if reverse('request-count') != request.META['PATH_INFO']:
            RequestLog(http_request=http_request).save()
