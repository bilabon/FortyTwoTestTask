# -*- coding: utf-8 -*-

from contact.models import Contact, ObjectLogEntry
from contact.tests.base import BaseSetup


class SignalProcessorTest(BaseSetup):
    '''
     Testing signal processor that, for every model, creates
     the db entry about the object creation/editing/deletion
    '''
    def setUp(self):
        super(SignalProcessorTest, self).setUp()

        Contact.objects.all().delete()
        ObjectLogEntry.objects.all().delete()
        self.contact, create = Contact.objects.get_or_create(
            id=777, date_of_birth='2015-10-20')

    def test_handle_object_save(self):
        '''
        Handle post_save signal, check action CREATE
        '''
        obj = ObjectLogEntry.objects.filter(
            object_name='Contact',
            action=ObjectLogEntry.CREATE)
        self.assertEqual(obj.count(), 1)

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
