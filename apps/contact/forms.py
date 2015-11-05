from django import forms
from django.forms import ModelForm, Textarea

from contact.models import Contact
from contact.widgets import AdminImageWidget, CalendarWidget


class ContactEditForm(ModelForm):
    date_of_birth = forms.DateField(widget=CalendarWidget)

    class Meta:
        model = Contact
        widgets = {
            'avatar': AdminImageWidget(),
            'bio': Textarea(attrs={'rows': 2}),
            'contacts': Textarea(attrs={'rows': 2}), }
