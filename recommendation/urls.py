from django.urls import path
from recommendation.views import create_product_flutter, show_main, show_recommendation, add_recommendation, get_recommendation_json, add_recommendation_ajax, get_user_inventory_json, get_book_image, add_recommendation_ajax, get_book_ids, search_recommendation, show_out_recommendation, outside_recommendation_add, get_out_recommendation_json, search_out_recommendation
app_name = 'recommendation'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('show-recommendation/', show_recommendation, name='show_recommendation'),
    path('show-out-recommendation/', show_out_recommendation, name='show_out_recommendation'),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path('get-recommendation-json/', get_recommendation_json, name='get_recommendation_json'),
    path('add-recommendation-ajax/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('get-user-inventory-json/', get_user_inventory_json, name='get_user_inventory_json'),
    path('get-book-image/', get_book_image, name='get_book_image'),
    path('add_recommendation_ajax/<int:bookId1>/<int:bookId2>/', add_recommendation_ajax, name='add_recommendation_ajax'),
    path('search-recommendation/', search_recommendation, name='search_recommendation'),
    path('get-book-ids/', get_book_ids, name='get_book_ids'),
    path('outside-recommendation-add/', outside_recommendation_add, name='outside_recommendation_add'),
    path('get-out-recommendation-json/', get_out_recommendation_json, name='get_out_recommendation_json'),
    path('search-out-recommendation/', search_out_recommendation, name='search_out_recommendation'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]