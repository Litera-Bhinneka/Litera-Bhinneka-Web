from django.urls import path
from manage_user.views import user_page
from manage_user.views import add_to_inventory
from manage_user.views import get_book_json, increment_book_ajax

app_name = 'manage_user'

urlpatterns = [
    path('user-page/', user_page, name='user_page'),
    path('add-to-inventory/', add_to_inventory, name='add_to_inventory'),
    path('get-book-json/', get_book_json, name='get_book_json'),
    path('increment-book-ajax/<int:book_id>/', increment_book_ajax, name='increment_book_ajax'),
    path('add-to-inventory/increment-book-ajax/<int:book_id>/', increment_book_ajax, name='increment_book_ajax'),

]