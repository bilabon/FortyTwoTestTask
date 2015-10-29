import os
import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from requests.models import RequestLog


class MiddlewareHandleTest(TestCase):
    '''
    Testing the SaveRequestMiddleware
    '''
    def test_middleware_handle_storing_request_log(self):
        '''
        Check that the middleware handle and store request at db
        '''
        RequestLog.objects.all().delete()
        self.client.get(reverse('home'))
        self.client.get(reverse('request-log'))
        self.client.get(reverse('request-log'))

        self.assertEqual(RequestLog.objects.count(), 3)
        self.assertEqual(RequestLog.objects.first().path_info, reverse('home'))
        self.assertEqual(
            RequestLog.objects.all()[1].path_info, reverse('request-log'))
