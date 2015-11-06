import os
import factory
import shutil

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = 'smith'
    password = factory.PostGenerationMethodCall('set_password', 'smith')
    is_active = True


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

        UserFactory.create()

    def tearDown(self):
        # remove CACHE folders
        for path in self.cache_dirs:
            shutil.rmtree(path)

    def test_initial(self):
        self.assertEqual(User.objects.count(), 2)
