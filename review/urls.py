from django.urls import path
from review.views import show_review, add_review, see_book_review, get_review_json, add_review_ajax

app_name = 'review'

urlpatterns = [
  path('show-review/', show_review, name='show_review'),
  path('add-review/', add_review, name='add_review'),
  path('book-review/<int:id>/', see_book_review, name='book_review'),
  path('get-review-json/<int:book_id>/', get_review_json, name='get_review_json'),
  path('add-review-ajax/<int:book_id>/', add_review_ajax, name='add_review_ajax'),
  path('book-review/<int:book_id1>/add-review-ajax/<int:book_id2>/', add_review_ajax, name='add_review_ajax'),

#   path('login/', login_user, name='login'), 
#   path('logout/', logout_user, name='logout'),
]