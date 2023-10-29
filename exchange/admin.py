from django.contrib import admin
from exchange.models import Offer, Meet

@admin.register(Offer)
class offerAdmin(admin.ModelAdmin):
    list_display = ['Username1',
                    'Username2',
                    'Inventory1',
                    'Inventory2']
    
@admin.register(Meet)
class meetAdmin(admin.ModelAdmin):
    list_display = ['sender',
                    'receiver',
                    'offer',
                    'date',
                    'location',
                    'message']