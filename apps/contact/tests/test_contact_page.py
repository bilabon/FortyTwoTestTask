# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

from contact.models import Contact
from contact.tests.base import BaseSetup


class ContactPageTest(BaseSetup):
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
        self.assertEqual('Some bio', contact.bio)
        self.assertEqual('John', contact.first_name)
        self.assertEqual('Smith', contact.last_name)
        self.assertEqual('Some contact', contact.contacts)
        self.assertEqual('2015-10-20', str(contact.date_of_birth))
        self.assertEqual('test_skype', contact.skype)
        self.assertEqual('test@jabber.com', contact.jabber)
        self.assertEqual('test@email.com', contact.email)

    def test_assert_other_data_at_page(self):
        '''
        Check present all contacts data on the home page
        '''
        response = self.client.get(reverse('home'))
        self.assertIn('Name: </span>John', response.content)
        self.assertIn('Surname: </span>Smith', response.content)
        self.assertIn('Date of birth: </span>10/20/2015', response.content)
        self.assertIn('Bio: </span><p>Some bio</p>', response.content)
        self.assertIn('Contacts: </span><p>Some contact</p>', response.content)
        self.assertIn('Email: </span>test@email.com', response.content)
        self.assertIn('Jabber: </span>test@jabber.com', response.content)
        self.assertIn('Skype: </span>test_skype', response.content)

    def test_cached_image_at_home_page(self):
        '''
        Checking if a cached image persist at home page
        '''
        response = self.client.get(reverse('home'))
        self.assertIn('/uploads/CACHE/images/image/8e042c66a0'
                      'd5d5bbb7ef96e35e305d08.png', response.content)

    def test_two_record_at_db(self):
        '''
        We have to show only first object at home page, check for it
        '''
        Contact.objects.create(date_of_birth='2011-11-11', first_name='Ali')
        self.assertEqual(Contact.objects.count(), 2)
        response = self.client.get(reverse('home'))
        self.assertIn('Date of birth: </span>10/20/2015', response.content)
        self.assertIn('Name: </span>John', response.content)

    def test_cyrillic_saving(self):
        '''
        Test showing cyrillic symbols at home page
        '''
        contact = Contact.objects.first()
        contact.first_name = u'Вася'
        contact.last_name = u'Бур'
        contact.save()
        response = self.client.get(reverse('home'))

        self.assertIn(smart_str(u'Вася'), response.content)
        self.assertIn(smart_str(u'Бур'), response.content)

    def test_empty_contact_model(self):
        '''
        Test in case we have none of Contact's objects in database
        '''
        Contact.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertIn('<p>Create Class object first</p>', response.content)
