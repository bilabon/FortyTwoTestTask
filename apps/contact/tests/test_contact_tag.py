# -*- coding: utf-8 -*-

from django.template import Context, Template
from contact.templatetags import contact_tags
from contact.models import Contact
from contact.tests.base import BaseSetup


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
