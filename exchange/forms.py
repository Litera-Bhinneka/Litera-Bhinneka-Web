from django.forms import ModelForm, Form
from django import forms
from exchange.models import Offer, Meet

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['Username1', 'Username2', 'Inventory1', 'Inventory2']

class MeetForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'w-full p-2 rounded border', 'type': 'date'}),
        label='date'
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full p-2 rounded border'}),
        label='location'
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-2 rounded border'}),
        label='message'
    )

    class Meta:
        model = Meet
        fields = ['date', 'location', 'message']