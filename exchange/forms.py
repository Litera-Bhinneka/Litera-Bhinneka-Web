from django.forms import ModelForm
from exchange.models import Offer

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['Username1', 'Username2', 'Inventory1', 'Inventory2']
