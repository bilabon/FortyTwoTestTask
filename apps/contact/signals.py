from django.core.signals import request_finished
from django.db import connection
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.transaction import TransactionManagementError
from django.core.exceptions import MultipleObjectsReturned
from contact.models import ObjectLogEntry

EXCLUDE_LIST = ['ObjectLogEntry', 'LogEntry']


@receiver(post_save)
def handle_object_save_and_update(sender, instance, created, **kwargs):
    if ObjectLogEntry._meta.db_table in connection.introspection.table_names():
        if sender.__name__ not in EXCLUDE_LIST:
            if created:
                action = ObjectLogEntry.CREATE
            else:
                action = ObjectLogEntry.UPDATE

            if isinstance(instance.pk, int):
                fields = {'object_name': sender.__name__,
                          'object_pk': instance.pk,
                          'action': action}
                ObjectLogEntry.objects.create(**fields)


@receiver(post_delete)
def handle_object_delete(sender, instance, **kwargs):
    if ObjectLogEntry._meta.db_table in connection.introspection.table_names():
        if sender.__name__ not in EXCLUDE_LIST:
            action = ObjectLogEntry.DELETE
            if isinstance(instance.pk, int):
                fields = {'object_name': sender.__name__,
                          'object_pk': instance.pk,
                          'action': action}
                ObjectLogEntry.objects.create(**fields)
