from django.urls import path
from exchange.views import show_books, offer_user, get_owners, add_offer, show_offers, delete_offer, accept_offer

app_name = 'exchange'

urlpatterns = [
    path('', show_books, name='show_books'),
    path('offer-user/<str:username>/', offer_user, name='offer_user'),
    path('get-owners/<int:id>/', get_owners, name='get_owners'),
    path('add-offer/', add_offer, name='add_offer'),
    path('show-offers/', show_offers, name='show_offers'),
    path('delete-offer/<int:id>/', delete_offer, name='delete_offer'),
    path('accept-offer/<int:id>/', accept_offer, name='accept_offer'),
]