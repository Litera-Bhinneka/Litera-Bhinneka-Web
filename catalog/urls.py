from django.urls import path
from catalog.views import show_catalog

app_name = 'catalog'

urlpatterns = [
  path('show-catalog/', show_catalog, name='show_catalog'),
#   path('add-review/', add_review, name='add_review'),
#   path('login/', login_user, name='login'), 
#   path('logout/', logout_user, name='logout'),
]