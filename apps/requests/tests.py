import json
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import RequestLog


class RequestPageTest(TestCase):
    """
    Testing response from home page
    """

    def test_exist_request_log_url(self):
        """
        Check main URL responce.
        """
        response = self.client.get(reverse('request-log'))
        self.assertEqual(response.status_code, 200)

    def test_saving_http_request_to_bd(self):
        """
        Check present my name, surname, date of birth, email, bio, contacts
        on the home page.
        """
        self.client.get(reverse('home'))
        self.client.get(reverse('request-log'))
        self.client.get(reverse('request-log'))
        self.assertEqual(RequestLog.objects.count(), 3)

    def test_api_request_count_started(self):
        """
        Testing request count api without log request
        """
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 0)

    def test_api_request_count_secont(self):
        """
        Testing request count api with 2 requests
        """
        self.client.get(reverse('home'))
        self.client.get(reverse('home'))
        response = self.client.get(
            reverse('request-count'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['request_count'], 2)
