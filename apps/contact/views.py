from django.views.generic import DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Contact
from .forms import ContactEditForm
from .utils import AjaxFormResponseMixin, get_object_or_json404


class HomeView(DetailView):
    '''
    View for home page. Return a Contact object for contact info.
    '''
    model = Contact
    template_name = 'home.html'

    def get_object(self, queryset=None):
        return Contact.objects.first()


class AjaxContactEditView(AjaxFormResponseMixin, UpdateView):

    form_class = ContactEditForm
    template_name = 'contact-edit.html'

    def get_object(self, queryset=None):
        # return get_object_or_json404(Contact, pk=self.kwargs['pk'])
        return Contact.objects.first()
