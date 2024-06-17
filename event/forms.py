import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from event.models import Event


class EventForm(forms.ModelForm):
    name = forms.CharField()
    max_participants = forms.IntegerField()
    description = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField()

    class Meta:
        model = Event
        fields = ["name", "max_participants", "description", "date", "location"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
