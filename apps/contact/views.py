from django.views.generic import DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from contact.models import Contact
from contact.forms import ContactEditForm
from contact.utils import AjaxFormResponseMixin


class HomeView(DetailView):
    '''
    View for home page. Return a Contact object for contact info.
    '''
    model = Contact
    template_name = 'home.html'

    def get_object(self, queryset=None):
        obj = Contact.objects.first()
        return obj


class AjaxContactEditView(AjaxFormResponseMixin, UpdateView):

    form_class = ContactEditForm
    template_name = 'contact-edit.html'

    def get_object(self, queryset=None):
        obj = Contact.objects.first()
        if not obj:
            obj = Contact.objects.create(date_of_birth='2015-10-22')
        return obj
