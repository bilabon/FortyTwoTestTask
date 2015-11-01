# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ObjectLogEntry'
        db.create_table(u'contact_objectlogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('object_pk', self.gf('django.db.models.fields.IntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'contact', ['ObjectLogEntry'])

    def backwards(self, orm):
        # Deleting model 'ObjectLogEntry'
        db.delete_table(u'contact_objectlogentry')


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
        },
        u'contact.objectlogentry': {
            'Meta': {'object_name': 'ObjectLogEntry'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']