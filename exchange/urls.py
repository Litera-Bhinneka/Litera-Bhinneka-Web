from django.urls import path
from exchange.views import *

app_name = 'exchange'

urlpatterns = [
    path('', show_books, name='show_books'),
    path('offer-user/<str:username>/', offer_user, name='offer_user'),
    path('get-owners/<int:id>/', get_owners, name='get_owners'),
    path('get-owners-flutter/<int:id>/<str:username>/', get_owners_flutter, name='get_owners_flutter'),
    path('add-offer/', add_offer, name='add_offer'),
    path('show-offers/', show_offers, name='show_offers'),
    path('get-inventories-flutter/<str:username1>/<str:username2>/', get_inventories_flutter, name='get_inventories_flutter'),
    path('create-offer-flutter/', create_offer_flutter, name='create_offer_flutter'),
    path('get-offers-flutter/<str:username>/', get_offers_flutter, name='get_offers_flutter'),
    path('detail-offer-flutter/<int:id>/', detail_offer_flutter, name='detail_offer_flutter'),
    path('delete-offer/<int:id>/', delete_offer, name='delete_offer'),
    path('delete-offer-flutter/', delete_offer_flutter, name='delete_offer_flutter'),
    path('accept-offer/<int:id>/', accept_offer, name='accept_offer'),
    path('accept-offer-flutter/', accept_offer_flutter, name='accept_offer_flutter'),
    path('schedule-meet/<int:id>/', schedule_meet, name='schedule_meet'),
]