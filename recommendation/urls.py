from django.urls import path
from recommendation.views import show_recommendation, add_recommendation, get_recommendation_json, add_recommendation_ajax, get_user_inventory_json, get_book_image

app_name = 'recommendation'

urlpatterns = [
    path('show-recommendation/', show_recommendation, name='show_recommendation'),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path('get-recommendation-json/', get_recommendation_json, name='get_recommendation_json'),
    path('add-recommendation-ajax/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('get-user-inventory-json/', get_user_inventory_json, name='get_user_inventory_json'),
    path('get-book-image/', get_book_image, name='get_book_image'),
]