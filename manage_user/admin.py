from django.contrib import admin
from manage_user.models import Inventory

# Register your models here.
@admin.register(Inventory)
class inventoryAdmin(admin.ModelAdmin):
   list_display=['user',
                'book',
                'amount',]
