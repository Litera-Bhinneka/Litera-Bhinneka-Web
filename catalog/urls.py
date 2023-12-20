from django.urls import path
from catalog.views import show_catalog
from catalog.views import get_product_json, add_product_ajax, search_books, edit_book, create_product_flutter, edit_product_flutter, get_product_by_id, delete_product_flutter

app_name = 'catalog'

urlpatterns = [
  path('show-catalog/', show_catalog, name='show_catalog'),
  path('get-product/', get_product_json, name='get_product_json'),
  path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
  path('search-books/', search_books, name='search_books'),
  path('show-catalog/edit-book/<int:id>/', edit_book, name='edit_book'),
  path('create-flutter/', create_product_flutter, name='create_product_flutter'),
  path('edit_product_flutter/<int:id>/', edit_product_flutter, name='edit_product_flutter'),
  path('get_product_id/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
  path('delete_product_flutter/<int:id>/', delete_product_flutter, name='delete_product_flutter'),

]