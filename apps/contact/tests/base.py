import os
import factory
import shutil
from mock import patch

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from contact.models import Contact


class FakeMiddleware(object):
    '''
    Fake empty middleware
    '''
    def process_request(self, request):
        return None


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = 'smith'
    password = factory.PostGenerationMethodCall('set_password', 'smith')
    is_active = True


class ContactFactory(factory.Factory):
    class Meta:
        model = Contact

    id = 1
    bio = "Some bio"
    first_name = "John"
    last_name = "Smith"
    contacts = "Some contact"
    date_of_birth = "2015-10-20"
    skype = "test_skype"
    jabber = "test@jabber.com"
    email = "test@email.com"
    avatar = "image.jpg"


class BaseSetup(TestCase):
    '''
    Base configs for tests
    '''

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'fixtures')

        self.cache_dirs = [
            os.path.join(settings.BASE_DIR, 'fixtures', 'CACHE'),
            os.path.join(settings.BASE_DIR, 'fixtures', 'avatars'), ]

        for path in self.cache_dirs:
            if not os.path.exists(path):
                os.makedirs(path)

        ContactFactory().save_base()
        UserFactory.create()

        self.patcher1 = patch(
            'apps.requests.middleware.SaveRequestMiddleware', FakeMiddleware)
        self.patcher1.start()

    def tearDown(self):
        self.patcher1.stop()
        # remove CACHE folders
        for path in self.cache_dirs:
            shutil.rmtree(path)

    def test_initial(self):
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)
