from django.test import TestCase
from django.core.urlresolvers import reverse


class ContactPageTest(TestCase):

    def test_exist_main_url(self):
        """
        Check main URL responce.
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_assert_data_at_main_url(self):
        """
        Check present my name, surname, date of birth, bio, contacts
        on the main page.
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.content, 'Dmytro')
        self.assertEqual(response.content, 'Bazas')
