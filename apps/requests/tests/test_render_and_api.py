import os
import json
import factory
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from requests.models import RequestLog


class RequestLogFactory(factory.Factory):
    class Meta:
        model = RequestLog

    path_info = factory.LazyAttribute(lambda a: '/some-url-{}/'.format(a.id))


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

    def test_requests_pagination(self):
        '''
        Test: return 10 latest objects at the page
        '''
        RequestLog.objects.all().delete()

        for pk in xrange(15):
            RequestLog.objects.create(id=pk)

        response = self.client.get(reverse('request-log'))

        # check count objects at page
        self.assertEqual(len(response.context['object_list']), 10)

        # check sorting objects at page
        for pk, index in zip(xrange(15, 5, -1), xrange(10)):
            self.assertEqual(response.context['object_list'][index].pk, pk)
