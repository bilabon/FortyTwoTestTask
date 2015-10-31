# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth.models import User


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RequestLog.method'
        db.alter_column(u'requests_requestlog', 'method', self.gf('django.db.models.fields.CharField')(max_length=20))
        #create initial user
        user = User.objects.create_user('user', 'babyx64@gmail.com', 'user')
        user.is_staff = True
        user.is_superuser = True
        user.save()

    def backwards(self, orm):

        # Changing field 'RequestLog.method'
        db.alter_column(u'requests_requestlog', 'method', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        u'requests.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'path_info': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'server_protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests']