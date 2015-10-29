import os
import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from requests.models import RequestLog


class RequestLogTest(TestCase):
    '''
    Testing response from request-log page
    '''

    def test_exist_request_log_url(self):
        '''
        Check responce status.
        '''
        response = self.client.get(reverse('request-log'))
        self.assertEqual(response.status_code, 200)

    def test_api_request_count_started(self):
        '''
        Testing API: requests count without log request
        '''
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 0)

    def test_api_request_count_secont(self):
        '''
        Testing API: request count with 2 requests
        '''
        self.client.get(reverse('home'))
        self.client.get(reverse('home'))
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 2)

    def test_requests_count_per_page(self):
        '''
        Should return 10 last requests at the page
        '''
        for index in xrange(15):
            self.client.get(reverse('request-log'))

        response = self.client.get(reverse('request-log'))
        request_count = response.content.count(str(RequestLog.objects.last()))
        self.assertEqual(request_count, 10)
