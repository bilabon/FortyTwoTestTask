from django.views.generic import DetailView
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
