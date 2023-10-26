from django.urls import path
from catalog.views import show_catalog
from catalog.views import get_product_json, add_product_ajax
app_name = 'catalog'

urlpatterns = [
  path('show-catalog/', show_catalog, name='show_catalog'),
#   path('add-review/', add_review, name='add_review'),
#   path('login/', login_user, name='login'), 
#   path('logout/', logout_user, name='logout'),
  path('get-product/', get_product_json, name='get_product_json'),
  path('create-product-ajax/', add_product_ajax, name='add_product_ajax')
  
]