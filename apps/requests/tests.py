import os
import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import RequestLog


class BaseTest(TestCase):
    fixtures = ['fixtures/contact.json']

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'fixtures')


class RequestPageTest(BaseTest):
    '''
    Testing response from home page
    '''

    def test_exist_request_log_url(self):
        '''
        Check main URL responce.
        '''
        response = self.client.get(reverse('request-log'))
        self.assertEqual(response.status_code, 200)

    def test_saving_http_request_to_bd(self):
        '''
        Check present my name, surname, date of birth, email, bio, contacts
        on the home page.
        '''
        self.client.get(reverse('home'))
        self.client.get(reverse('request-log'))
        self.client.get(reverse('request-log'))
        self.assertEqual(RequestLog.objects.count(), 3)

    def test_api_request_count_started(self):
        '''
        Testing request count api without log request
        '''
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 0)

    def test_api_request_count_secont(self):
        '''
        Testing request count api with 2 requests
        '''
        self.client.get(reverse('home'))
        self.client.get(reverse('home'))
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 2)

    def test_request_default_ordering(self):
        '''
        Tesing default ordering for request
        '''
        RequestLog.objects.all().delete()
        response = self.client.get(reverse('home'))
        obj = RequestLog.objects.first()
        obj.priority = 1
        obj.save()

        for index in xrange(10):
            self.client.get(reverse('request-log'))

        # Now we have 11 records at RequestLog model and paginate_by = 10,
        # so we check if firts record with priority=1 exist in template
        response = self.client.get(reverse('request-log'))
        self.assertNotIn(
            'Priority: 1 | Request GET %s' % reverse('home'), response.content)

    def test_request_priority_1_ordering(self):
        '''
        Tesing ordering by get parameter ?priority=1
        '''
        RequestLog.objects.all().delete()
        response = self.client.get(reverse('home'))
        obj = RequestLog.objects.first()
        obj.priority = 1
        obj.save()

        for index in xrange(10):
            self.client.get(reverse('request-log'))

        # Now we have 11 records at RequestLog model and paginate_by = 10,
        # so we check if firts record with priority=1 exist in template
        response = self.client.get(reverse('request-log'), {'priority': 1})
        self.assertIn(
            'Priority: 1 | Request GET %s' % reverse('home'), response.content)
