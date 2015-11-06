import os
import json
import factory
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from requests.models import RequestLog


class RequestLogFactory(factory.Factory):
    FACTORY_FOR = RequestLog

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
            RequestLogFactory(id=pk).save_base()

        response = self.client.get(reverse('request-log'))

        # check count objects at page
        self.assertEqual(len(response.context['object_list']), 10)

        # check sorting objects at page
        obj_list_sorted = RequestLog.objects.all().order_by('-timestamp',)[:10]
        self.assertQuerysetEqual(
            response.context['object_list'],
            [repr(obj) for obj in obj_list_sorted]
        )

    def test_update_viewed_field(self):
        '''
        Emulating GET request and check request_count then emulating
        POST request and after that check request count through GET request
        '''
        RequestLog.objects.all().delete()
        # generate 1 objects with viewed=True
        RequestLogFactory(id=1, viewed=True).save_base()

        # generate 15 objects with viewed=False
        for pk in xrange(2, 17):
            RequestLogFactory(id=pk).save_base()

        # check request_count through GET request
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 15)

        # after a POST request the request_count must equal 0
        self.client.post(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check request_count
        self.assertEqual(json.loads(response.content)['request_count'], 0)
