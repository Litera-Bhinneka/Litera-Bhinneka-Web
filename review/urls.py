from django.urls import path
from review.views import show_review, add_review, see_book_review, get_review_json, add_review_ajax, get_book_json, get_wishlist_json, add_review_flutter

app_name = 'review'

urlpatterns = [
  path('show-review/', show_review, name='show_review'),
  path('add-review/', add_review, name='add_review'),
  path('book-review/<int:id>/', see_book_review, name='book_review'),
  path('get-review-json/<int:book_id>/', get_review_json, name='get_review_json'),
  path('get-book-json/<int:book_id>/', get_book_json, name='get_book_json'),
  # path('add-review-ajax/<int:book_id>/', add_review_ajax, name='add_review_ajax'),
  path('book-review/<int:book_id1>/add-review-ajax/<int:book_id2>/', add_review_ajax, name='add_review_ajax'),
  path('get-wishlist-json/<int:book_id>/', get_wishlist_json, name='get_wishlist_json'),
  path('add-review-flutter/', add_review_flutter, name='add_review_flutter'),

#   path('login/', login_user, name='login'), 
#   path('logout/', logout_user, name='logout'),
]