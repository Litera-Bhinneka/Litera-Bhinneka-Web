from django.shortcuts import render, get_object_or_404
from catalog.models import Book
from manage_user.models import Inventory, Wishlist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def user_page(request):
    books = Book.objects.all().values()
    context = {
        'books': books,
        'name': request.user.username,
    }

    return render(request, "user_page.html", context)


def add_to_inventory(request):
    books = Book.objects.all().values()
    context = {
        'books': books,
        'name': request.user.username,
    }

    return render(request, "add_to_inventory.html", context)


def get_book_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))


@csrf_exempt
def increment_book_ajax(request, book_id):
    print(request.method)
    book = Book.objects.get(pk=book_id)
    user = request.user

    # Create or increment the Inventory object
    inventory, created = Inventory.objects.get_or_create(user=user, book=book)
    if not created:
        inventory.amount += 1
        inventory.save()
        
    return HttpResponse(b"DELETED", status=201)

def add_wishlist(request, book_id):
    if request.method =="POST":
        book = Book.objects.get(pk=book_id)
        user = request.user
        new_wishlist = Wishlist(user=user,
                              book=book)
        new_wishlist.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def remove_wishlist(request, book_id):
    if request.method =="DELETE":
        book = Book.objects.get(pk=book_id)
        user = request.user
        Wishlist.objects.filter(user=user, book=book).delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()
        
# @csrf_exempt
# def add_review_ajax(request, book_id1, book_id2):
#     if request.method == 'POST':
#         print(request.POST)
#         print(request.POST.get("rating"))
#         review_text = request.POST.get("review_text")
#         review_summary = request.POST.get("review_summary")
#         reviewer_name = request.user.username
#         rating = int(request.POST.get("review_score"))
#         book_title = get_object_or_404(Book, pk=book_id2).title

#         new_review = Review(book_title=book_title,
#                              reviewer_name=reviewer_name, 
#                              review_score=rating,
#                              review_summary=review_summary,
#                              review_text=review_text)
#         new_review.save()

#         return HttpResponse(b"CREATED", status=201)
#     print(request.method)

#     return HttpResponseNotFound()
