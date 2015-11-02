import os
from mock import patch
from django.conf import settings
from django.test import TestCase


class FakeMiddleware(object):
    '''
    Fake empty middleware
    '''
    def process_request(self, request):
        return None


class BaseSetup(TestCase):
    '''
    Base configs for tests
    '''
    fixtures = ['fixtures/contact.json']

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'fixtures')

        self.patcher1 = patch(
            'apps.requests.middleware.SaveRequestMiddleware', FakeMiddleware)
        self.patcher1.start()

    def tearDown(self):
        self.patcher1.stop()
