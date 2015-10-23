import os
import json
from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .models import Contact


class BaseTest(TestCase):
    fixtures = ['fixtures/contact.json']

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'fixtures')


class ContactPageTest(BaseTest):
    '''
    Testing response from home page
    '''

    def test_page_exist(self):
        '''
        Check page exist.
        '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_data_at_database(self):
        '''
        Check data at database
        '''
        contact = Contact.objects.first()
        self.assertEqual('John', contact.first_name)
        self.assertEqual('test@email.com', contact.email)
        self.assertEqual('test_skype', contact.skype)

    def test_assert_other_data_at_page(self):
        '''
        Check present all contacts data on the home page
        '''
        response = self.client.get(reverse('home'))
        self.assertIn('Name: </span>John', response.content)
        self.assertIn('Surname: </span>Smith', response.content)
        self.assertIn('Date of birth: </span>10/20/2015', response.content)
        self.assertIn('Bio: </span>Some bio', response.content)
        self.assertIn('Contacts: </span>Some contact', response.content)
        self.assertIn('Email: </span>test@email.com', response.content)
        self.assertIn('Jabber: </span>test@jabber.com', response.content)
        self.assertIn('Skype: </span>test_skype', response.content)

    def test_cached_image_at_home_page(self):
        '''
        Checking if a cached image persist at home page
        '''
        response = self.client.get(reverse('ajax_contact_edit_view'))
        self.assertIn('/uploads/CACHE/images/image/8e042c66a0'
                      'd5d5bbb7ef96e35e305d08.png', response.content)


class ContactEditTest(BaseTest):
    '''
    Testing response from home page
    '''

    def test_page_exist(self):
        '''
        Check page exist
        '''
        response = self.client.get(reverse('ajax_contact_edit_view'))
        self.assertEqual(response.status_code, 200)

    def test_cached_image_at_contacts_edit_page(self):
        '''
        Checking if a cached image persist at contacts edit page
        '''
        response = self.client.get(reverse('ajax_contact_edit_view'))
        self.assertIn('/uploads/CACHE/images/image/8e042c66a0'
                      'd5d5bbb7ef96e35e305d08.png', response.content)

    def test_assert_other_data_at_page(self):
        '''
        Check present all contacts data on the contacts edit page
        '''
        response = self.client.get(reverse('ajax_contact_edit_view'))
        self.assertIn('value="John"', response.content)
        self.assertIn('value="Smith"', response.content)
        self.assertIn('value="2015-10-20"', response.content)
        self.assertIn('Some bio', response.content)
        self.assertIn('Some contact', response.content)
        self.assertIn('value="test@email.com"', response.content)
        self.assertIn('value="test@jabber.com"', response.content)
        self.assertIn('value="test_skype"', response.content)

    def test_bad_responce_updating_data(self):
        '''
        Checking for error if required field was not specified
        '''
        data = {}
        client = Client()
        response = client.post(reverse('ajax_contact_edit_view'), data=data)
        resp_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_dict['date_of_birth'][0],
                         'This field is required.')

    def test_updating_date_of_birth(self):
        '''
        Updating date_of_birth field
        '''
        data = {'date_of_birth': '2014-10-22'}
        client = Client()
        response = client.post(reverse('ajax_contact_edit_view'), data=data)
        resp_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(resp_dict['success'])

        contact = Contact.objects.first()
        self.assertEqual(data['date_of_birth'], str(contact.date_of_birth))
