import json
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import RequestLog


class ContactPageTest(TestCase):
    """
    Testing response from home page
    """
    fixtures = ['fixtures/user.json']

    def test_exist_home_url(self):
        """
        Check main URL responce.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_assert_data_on_home_url(self):
        """
        Check present my name, surname, date of birth, email, bio, contacts
        on the home page.
        """
        response = self.client.get(reverse('home'))
        self.assertIn('Name: </span>John', response.content)
        self.assertIn('Surname: </span>Smith', response.content)
        self.assertIn('Date of birth: </span>10/15/2015', response.content)
        self.assertIn('Email: </span>test@example.com', response.content)
        self.assertIn('Bio: </span>some bio', response.content)
        self.assertIn('Contacts: </span>some contacts', response.content)


class RequestPageTest(TestCase):
    """
    Testing response from home page
    """
    fixtures = ['fixtures/user.json']

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
