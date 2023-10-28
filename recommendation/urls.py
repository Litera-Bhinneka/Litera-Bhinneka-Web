from django.urls import path
from recommendation.views import show_recommendation, add_recommendation, get_recommendation_json, add_recommendation_ajax, get_user_inventory_json, get_book_image, add_recommendation_ajax, get_book_ids, search_recommendation

app_name = 'recommendation'

urlpatterns = [
    path('show-recommendation/', show_recommendation, name='show_recommendation'),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path('get-recommendation-json/', get_recommendation_json, name='get_recommendation_json'),
    path('add-recommendation-ajax/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('get-user-inventory-json/', get_user_inventory_json, name='get_user_inventory_json'),
    path('get-book-image/', get_book_image, name='get_book_image'),
    path('add_recommendation_ajax/<int:bookId1>/<int:bookId2>/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('search-recommendation/', search_recommendation, name='search_recommendation'),
    path('get-book-ids/', get_book_ids, name='get_book_ids'),
]