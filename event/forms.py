import datetime

from django import forms


class EventForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.CharField()
