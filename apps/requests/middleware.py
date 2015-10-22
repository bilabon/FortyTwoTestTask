from django.conf import settings
from django.core.urlresolvers import reverse

from .models import RequestLog


class SaveRequestMiddleware(object):
    """
    Custom middleware for saving all http requests to database
    """
    def process_request(self, request):
        path_info = request.META['PATH_INFO']
        if (reverse('request-count') not in path_info and
           settings.MEDIA_URL not in path_info):
            new_http_request = RequestLog()
            new_http_request.method = request.META['REQUEST_METHOD']
            new_http_request.path_info = path_info
            new_http_request.server_protocol = request.META['SERVER_PROTOCOL']
            new_http_request.save()
