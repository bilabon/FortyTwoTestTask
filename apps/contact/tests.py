# -*- coding: utf-8 -*-

import os
import json
from StringIO import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.core.urlresolvers import reverse

from django.template import Context, Template
from django.test import TestCase, Client

from .templatetags import contact_tags
from .models import Contact, ObjectLogEntry
from django.utils.encoding import smart_str


class BaseSetup(TestCase):
    fixtures = ['fixtures/contact.json']

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'fixtures')


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
        response = self.client.get(reverse('ajax_contact_edit_view'))
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


class ContactEditTest(BaseSetup):
    '''
    Tests for editing Contact model
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


class ContactTagTest(BaseSetup):
    '''
    Testing custom contact tags
    '''
    def test_admin_url_tag(self):
        '''
        Tag that accepts any object and renders the link to its admin edit page
        '''
        contact = Contact.objects.first()

        template = '{% admin_url contact %}'
        context = {'contact': contact}

        t = Template('{% load contact_tags %}' + template)
        c = Context(context)
        self.assertEqual(t.render(c), contact_tags.admin_url(contact))


class SignalProcessorTest(TestCase):
    '''
     Testing signal processor that, for every model, creates
     the db entry about the object creation/editing/deletion
    '''
    def setUp(self):
        self.contact = Contact(id=777, date_of_birth='2015-10-20')
        self.contact.save()

    def test_handle_object_save(self):
        '''
        Handle post_save signal, check action CREATE
        '''
        obj = ObjectLogEntry.objects.filter(
            object_name='Contact',
            action=ObjectLogEntry.CREATE)
        self.assertEqual(obj.count(), 2)

    def test_handle_object_update(self):
        '''
        Handle post_save signal, check action UPDATE
        '''
        self.contact.date_of_birth = '2015-05-15'
        self.contact.save()

        obj = ObjectLogEntry.objects.filter(
            object_name='Contact',
            action=ObjectLogEntry.UPDATE)
        self.assertEqual(obj.count(), 1)

    def test_handle_object_delete(self):
        '''
        Handle post_delete signal, check action DELETE
        '''
        Contact.objects.get(id=777).delete()

        obj = ObjectLogEntry.objects.filter(
            object_name='Contact',
            action=ObjectLogEntry.DELETE)
        self.assertEqual(obj.count(), 1)


class CommandTests(TestCase):
    '''
    Test infomodels command that prints all project models and
    the count of objects in every model.
    '''

    def test_command_infomodels_stdout(self):
        '''
        Testing stdout of command.
        '''
        stdout = StringIO()
        call_command('infomodels', stdout=stdout)
        for ct in ContentType.objects.all():
            m = ct.model_class()
            line = "%s.%s\t%d" % (
                m.__module__, m.__name__, m._default_manager.count())
            self.assertIn(line, stdout.getvalue())

    def test_command_infomodels_stderr(self):
        '''
        Testing stderr of command.
        '''
        stderr = StringIO()
        call_command('infomodels', stderr=stderr)
        for ct in ContentType.objects.all():
            m = ct.model_class()
            line = "%s.%s\t%d" % (
                m.__module__, m.__name__, m._default_manager.count())
            self.assertIn('Error: %s' % line, stderr.getvalue())

    def test_exeption_not_allow_any_args(self):
        '''
        Raise CommandError: The command does not allow any args
        '''
        self.assertRaises(CommandError, call_command, 'infomodels args')
