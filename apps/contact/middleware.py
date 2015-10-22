from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import format

from .utils import JsonNotFound
from .utils import render_to_json_response


class ExceptionMiddleware(object):
    '''Exception for JsonNotFound type'''
    def process_exception(self, request, exception):
        if type(exception) == JsonNotFound:
            now = format(timezone.now(), u'U')
            kwargs = {}
            response = {
                'status': '404',
                'message': 'Record not found',
                'timestamp': now,
                'errorcode': 'E404'
            }
            return render_to_json_response(response, status=404, **kwargs)
        return None