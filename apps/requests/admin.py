from django.contrib import admin
from django.db.models import Q

from .models import RequestLog


class PriorityListFilter(admin.SimpleListFilter):
    title = 'Priority'
    parameter_name = 'priority'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Order by priority'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.order_by('-priority', '-timestamp',)
        else:
            return queryset.order_by('-timestamp',)


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'timestamp', 'priority',)
    date_hierarchy = 'timestamp'
    list_filter = (PriorityListFilter, )

admin.site.register(RequestLog, RequestLogAdmin)
