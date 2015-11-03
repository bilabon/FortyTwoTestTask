import os
import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from requests.models import RequestLog


class RequestPriorityLogTest(TestCase):
    '''
    Testing response from request-log page
    '''
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
        self.assertEqual(response.context['object_list'][0].priority, 1)
