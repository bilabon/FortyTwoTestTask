# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Contact.user'
        db.delete_column(u'contact_contact', 'user_id')

        # Adding field 'Contact.first_name'
        db.add_column(u'contact_contact', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Contact.last_name'
        db.add_column(u'contact_contact', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Contact.email'
        db.add_column(u'contact_contact', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Contact.jabber'
        db.add_column(u'contact_contact', 'jabber',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Contact.skype'
        db.add_column(u'contact_contact', 'skype',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'Contact.avatar'
        db.add_column(u'contact_contact', 'avatar',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Contact.bio'
        db.alter_column(u'contact_contact', 'bio', self.gf('django.db.models.fields.TextField')(max_length=500))

        # Changing field 'Contact.contacts'
        db.alter_column(u'contact_contact', 'contacts', self.gf('django.db.models.fields.TextField')(max_length=500))

    def backwards(self, orm):
        # Adding field 'Contact.user'
        db.add_column(u'contact_contact', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['auth.User'], unique=True),
                      keep_default=False)

        # Deleting field 'Contact.first_name'
        db.delete_column(u'contact_contact', 'first_name')

        # Deleting field 'Contact.last_name'
        db.delete_column(u'contact_contact', 'last_name')

        # Deleting field 'Contact.email'
        db.delete_column(u'contact_contact', 'email')

        # Deleting field 'Contact.jabber'
        db.delete_column(u'contact_contact', 'jabber')

        # Deleting field 'Contact.skype'
        db.delete_column(u'contact_contact', 'skype')

        # Deleting field 'Contact.avatar'
        db.delete_column(u'contact_contact', 'avatar')


        # Changing field 'Contact.bio'
        db.alter_column(u'contact_contact', 'bio', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Contact.contacts'
        db.alter_column(u'contact_contact', 'contacts', self.gf('django.db.models.fields.TextField')())

    models = {
        u'contact.contact': {
            'Meta': {'object_name': 'Contact'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']