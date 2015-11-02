# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.test import Client

from contact.models import Contact
from contact.tests.base import BaseSetup


class ContactEditTest(BaseSetup):
    '''
    Tests for editing Contact model
    '''
    def setUp(self):
        super(ContactEditTest, self).setUp()
        self.client.login(username='smith', password='smith')

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

    def test_submit_ajax_form(self):
        '''
        Test submiting the ajax form with cyrillic data
        '''
        data = {
            'first_name': u'Вова',
            'last_name': u'Тест',
            'date_of_birth': '2014-10-23',
            'bio': u'Тест',
            'contacts': u'Тест',
            'email': u'test@test.com',
            'jabber': u'test@test.com',
            'skype': u'Тест', }

        client = Client()
        response = client.post(reverse('ajax_contact_edit_view'), data=data)
        resp_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(resp_dict['success'])

        contact = Contact.objects.first()
        self.assertEqual(data['date_of_birth'], str(contact.date_of_birth))
        self.assertEqual(data['first_name'], unicode(contact.first_name))
        self.assertEqual(data['last_name'], unicode(contact.last_name))
        self.assertEqual(data['bio'], unicode(contact.bio))
        self.assertEqual(data['contacts'], unicode(contact.contacts))
        self.assertEqual(data['email'], contact.email)
        self.assertEqual(data['jabber'], contact.jabber)
        self.assertEqual(data['skype'], unicode(contact.skype))
