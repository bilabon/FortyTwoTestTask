from django import forms
from django.forms import ModelForm, Textarea

from .models import Contact
from .widgets import AdminImageWidget, CalendarWidget


class UpdateContactForm(ModelForm):
    date_of_birth = forms.DateField(widget=CalendarWidget)

    class Meta:
        model = Contact
        widgets = {
            'avatar': AdminImageWidget(),
            'bio': Textarea(attrs={'rows': 2}),
            'contacts': Textarea(attrs={'rows': 2}), }