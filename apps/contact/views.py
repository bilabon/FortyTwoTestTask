import json
from django.http import HttpResponse, Http404
from django.views.generic import View, DetailView, ListView
from .models import Contact


class HomeView(DetailView):
    """
    View for home page. Return a Contact object for contact info.
    """
    model = Contact
    template_name = 'home.html'

    def get_object(self, queryset=None):
        return Contact.objects.first()
