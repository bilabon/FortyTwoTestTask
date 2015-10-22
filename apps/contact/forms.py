from django import forms
from django.forms import ModelForm, Textarea

from datetimewidget.widgets import DateWidget

from .models import Contact
from .widgets import AdminImageWidget


class UpdateContactForm(ModelForm):
    date_of_birth = forms.DateField(widget=DateWidget(
        bootstrap_version=3,
        options={'format': 'yyyy-mm-dd'},),)

    class Meta:
        model = Contact
        widgets = {
            'avatar': AdminImageWidget(),
            'bio': Textarea(attrs={'rows': 2}),
            'contacts': Textarea(attrs={'rows': 2}), }
