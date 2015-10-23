from django.contrib import admin

from .models import Contact, ObjectLogEntry


admin.site.register(Contact)
admin.site.register(ObjectLogEntry)
