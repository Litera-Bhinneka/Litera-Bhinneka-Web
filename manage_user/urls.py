from django.urls import path
from manage_user.views import user_page
from manage_user.views import add_to_inventory
from manage_user.views import get_book_json, increment_book_ajax, add_wishlist, remove_wishlist, show_wishlist, show_inventory, get_wishlist_json, remove_wishlist_sec, add_to_inventory_flutter, show_inventory_flutter, add_to_wishlist_flutter, show_wishlist_flutter
app_name = 'manage_user'

urlpatterns = [
    path('user-page/', user_page, name='user_page'),
    path('add-to-inventory/', add_to_inventory, name='add_to_inventory'),
    path('add-to-inventory-flutter/<int:book_id>/', add_to_inventory_flutter, name='add_to_inventory_flutter'),  
    path('get-book-json/', get_book_json, name='get_book_json'),
    path('increment-book-ajax/<int:book_id>/', increment_book_ajax, name='increment_book_ajax'),
    path('add-wishlist/<int:book_id>/', add_wishlist, name='add_wishlist'),
    path('add-to-wishlist-flutter/<int:book_id>/', add_to_wishlist_flutter, name='add_to_wishlist_flutter'),  
    path('remove-wishlist/<int:book_id>/', remove_wishlist, name='remove_wishlist'),
    path('get-wishlist-json/', get_wishlist_json, name='get_wishlist_json'),
    path('show-wishlist/', show_wishlist, name='show_wishlist'),
    path('show-wishlist-flutter/', show_wishlist_flutter, name='show_wishlist_flutter'),  
    path('show-inventory/', show_inventory, name='show_inventory'),
    path('show-inventory-flutter/', show_inventory_flutter, name='show_inventory_flutter'),  
    path('remove-wishlist-sec/<int:book_id>/', remove_wishlist_sec, name='remove_wishlist_sec'),
]