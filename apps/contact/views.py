import json
from django.http import HttpResponse, Http404
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.models import User

from .models import RequestLog


class HomeView(DetailView):
    """
    View for home page. Return User object for contact info.
    """
    model = User
    template_name = 'home.html'

    def get_object(self, queryset=None):
        obj = User.objects.first()
        return obj


class RequestLogListView(ListView):
    """
    Render page with 10 http requests and return http request count.
    """
    model = RequestLog
    paginate_by = 10
    template_name = 'request-log.html'

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
