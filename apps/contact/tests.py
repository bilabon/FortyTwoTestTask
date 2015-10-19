from django.test import TestCase
from django.core.urlresolvers import reverse


class ContactPageTest(TestCase):
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
