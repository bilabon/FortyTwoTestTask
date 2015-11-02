from django.conf import settings
from django.core.urlresolvers import reverse

from .models import RequestLog


class SaveRequestMiddleware(object):
    '''
    Custom middleware for saving all http requests to database
    '''
    def process_request(self, request):

        path_info = request.META['PATH_INFO']

        exlude_list = [reverse('request-count'),
                       reverse('admin:jsi18n'),
                       settings.MEDIA_URL,
                       settings.STATIC_URL]

        if not any(url in path_info for url in exlude_list):
            new_http_request = RequestLog()
            new_http_request.method = request.META['REQUEST_METHOD']
            new_http_request.path_info = path_info
            new_http_request.server_protocol = request.META['SERVER_PROTOCOL']
            new_http_request.priority = 0
            new_http_request.save()
