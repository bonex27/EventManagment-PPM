import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from event.models import Event


class EventForm(forms.Form):

    name = forms.CharField()
    max_participants = forms.IntegerField()
    description = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'Submit'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))

    class Meta:
        model = Event
        fields = '__all__'
