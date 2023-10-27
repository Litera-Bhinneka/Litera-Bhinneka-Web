from django.contrib import admin
from exchange.models import Offer

@admin.register(Offer)
class offerAdmin(admin.ModelAdmin):
    list_display = ['Username1',
                    'Username2',
                    'Inventory1',
                    'Inventory2']