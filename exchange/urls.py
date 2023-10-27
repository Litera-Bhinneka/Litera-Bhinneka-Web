from django.urls import path
from exchange.views import show_users, offer_user, get_books, add_offer, show_offers, delete_offer, accept_offer

app_name = 'exchange'

urlpatterns = [
    path('', show_users, name='show_users'),
    path('offer-user/<str:username>/', offer_user, name='offer_user'),
    path('get-books/<str:username>/', get_books, name='get_books'),
    path('add-offer/', add_offer, name='add_offer'),
    path('show-offers/', show_offers, name='show_offers'),
    path('delete-offer/<int:id>/', delete_offer, name='delete_offer'),
    path('accept-offer/<int:id>/', accept_offer, name='accept_offer'),
]