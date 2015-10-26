import json
from django.http import HttpResponse, Http404
from django.views.generic import View, ListView
from django.contrib.auth.models import User

from .models import RequestLog


class RequestLogListView(ListView):
    """
    Render page with 10 http requests and return http request count.
    """
    model = RequestLog
    paginate_by = 10
    template_name = 'request-log.html'
    ordering = ["-timestamp", ]

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        ordering = ["-timestamp", ]
        priority = self.request.GET.get('priority')

        if priority and priority == '1':
            ordering.insert(0, "-priority")
        return tuple(ordering)

    def get_queryset(self):
        queryset = super(RequestLogListView, self).get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequestLogListView, self).get_context_data(**kwargs)
        context['request_count'] = RequestLog.objects.count()
        return context


class RequestCountView(View):
    """Return count of http requests"""

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = {}
            mimetype = 'application/json'
            context['request_count'] = RequestLog.objects.count()
            data = json.dumps(context)
            return HttpResponse(data, mimetype)
        else:
            raise Http404
