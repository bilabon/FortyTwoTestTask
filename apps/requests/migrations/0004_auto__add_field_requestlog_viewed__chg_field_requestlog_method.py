# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestLog.viewed'
        db.add_column(u'requests_requestlog', 'viewed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'RequestLog.method'
        db.alter_column(u'requests_requestlog', 'method', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):
        # Deleting field 'RequestLog.viewed'
        db.delete_column(u'requests_requestlog', 'viewed')


        # Changing field 'RequestLog.method'
        db.alter_column(u'requests_requestlog', 'method', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'requests.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path_info': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'server_protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['requests']