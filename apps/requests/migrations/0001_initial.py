# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth.models import User


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestLog'
        db.create_table(u'requests_requestlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('path_info', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('server_protocol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'requests', ['RequestLog'])

        #create initial user

        user = User.objects.create_user('user', 'babyx64@gmail.com', 'user')
        user.is_staff = True
        user.is_superuser = True
        user.save()


    def backwards(self, orm):
        # Deleting model 'RequestLog'
        db.delete_table(u'requests_requestlog')


    models = {
        u'requests.requestlog': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'RequestLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path_info': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'server_protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests']