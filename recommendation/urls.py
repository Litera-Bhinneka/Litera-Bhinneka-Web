from django.urls import path
from recommendation.views import show_recommendation, add_recommendation, find_book_id, get_recommendation_json

app_name = 'recommendation'

urlpatterns = [
    path('show-recommendation/', show_recommendation, name='show_recommendation'),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path('find-book-id/<str:name>/', find_book_id, name='find_book_id'),
    path('get-recommendation-json/', get_recommendation_json, name='get_recommendation_json')
]