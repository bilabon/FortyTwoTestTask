import json
from django.http import HttpResponse, Http404
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.models import User


class HomeView(DetailView):
    """
    View for home page. Return User object for contact info.
    """
    model = User
    template_name = 'home.html'

    def get_object(self, queryset=None):
        obj = User.objects.first()
        return obj
