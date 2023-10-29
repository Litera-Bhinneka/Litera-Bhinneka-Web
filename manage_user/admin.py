from django.contrib import admin
from manage_user.models import Inventory, Wishlist

# Register your models here.
@admin.register(Inventory)
class inventoryAdmin(admin.ModelAdmin):
   list_display=['user',
                'book',
                'amount',]
   
@admin.register(Wishlist)
class wishlistAdmin(admin.ModelAdmin):
   list_display=['user',
                'book',]
