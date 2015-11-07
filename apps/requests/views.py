import json
from django.http import HttpResponse, Http404
from django.views.generic import View, ListView
from django.contrib.auth.models import User

from .models import RequestLog


class HandleOrderingMixin(object):

    ordering = ['-timestamp', ]

    def get_ordering(self):
        '''
        Return the field or fields to use for ordering the queryset.
        '''
        ordering = self.ordering
        return tuple(ordering)


class RequestLogListView(HandleOrderingMixin, ListView):
    '''
    Render page with 10 http requests and return http request count.
    '''
    model = RequestLog
    paginate_by = 10
    template_name = 'request-log.html'

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


class RequestCountView(HandleOrderingMixin, View):
    '''
    Updateing RequestLog objects based on GET viewed parameter.
    '''

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = {}
            mimetype = 'application/json'
            queryset = RequestLog.objects.filter(viewed=False)
            context['request_count'] = queryset.count()

            if self.request.GET.get('viewed') == 'true':
                queryset.update(viewed=True)
                queryset = RequestLog.objects.all()
                context['request_count'] = 0

            ordering = self.get_ordering()
            if ordering:
                queryset = queryset.order_by(*ordering)

            data = []
            for obj in queryset[:10]:
                data.append({
                    'priority': obj.priority,
                    'title': obj.__str__(),
                    'timestamp': obj.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'viewed': unicode(obj.viewed),
                    'id': obj.id,
                })

            context['object_list'] = data
            data = json.dumps(context)
            return HttpResponse(data, mimetype)
