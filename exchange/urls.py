from django.urls import path
from exchange.views import show_users, offer_user, get_books

app_name = 'exchange'

urlpatterns = [
    path('', show_users, name='show_users'),
    path('offer-user/<str:username>/', offer_user, name='offer_user'),
    path('get-books/<str:username>/', get_books, name='get_books'),
]