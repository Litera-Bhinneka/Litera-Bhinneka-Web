from django.shortcuts import render, get_object_or_404
from catalog.models import Book
from manage_user.models import Inventory, Wishlist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import template

register = template.Library()

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
@login_required(login_url='/authentication/login/')
def increment_book_ajax(request, book_id):
    if request.method == "POST":
        try:
            book = Book.objects.get(pk=book_id)
            user = request.user

            # Check if the book is already in the user's inventory
            inventory = Inventory.objects.filter(user=user, book=book).first()

            if inventory is None:
                # If not in inventory, create a new inventory entry
                inventory = Inventory(user=user, book=book, amount=1)
            else:
                # If already in inventory, increment the quantity
                inventory.amount += 1

            inventory.save()
            return HttpResponse(b"OK", status=201)

        except Book.DoesNotExist:
            return HttpResponseNotFound("Book not found")

    return HttpResponseNotFound("Invalid request")

def add_wishlist(request, book_id):
    if request.method =="POST":
        book = Book.objects.get(pk=book_id)
        user = request.user
        new_wishlist = Wishlist(user=user,
                              book=book)
        new_wishlist.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def remove_wishlist_sec(request, book_id):
    if request.method == "DELETE":
        wishlist_items = Wishlist.objects.filter(user=request.user, book__pk=book_id)
        print(wishlist_items)
        wishlist_items.delete()
        return HttpResponse(b"OK", status=200)
    
    return HttpResponseNotFound(b"Method not allowed for this endpoint", status=405)

@login_required(login_url='/authentication/login/')
def remove_wishlist(request, book_id):
    user = request.user
    try:
        # Dapatkan objek Wishlist yang sesuai dengan user dan buku
        wishlist = Wishlist.objects.get(user=user, book_id=book_id)
        # Hapus objek Wishlist tersebut
        wishlist.delete()
        return HttpResponseRedirect(reverse('user_page'))  # Ganti dengan URL yang sesuai
    except Wishlist.DoesNotExist:
        # Handle jika objek Wishlist tidak ditemukan
        return HttpResponseNotFound("Wishlist item not found")
    
def get_wishlist_json(request):
    user = request.user
    wishlist_books = Wishlist.objects.filter(user=user).values('book')
    books = Book.objects.filter(pk__in=wishlist_books)
    wishlist_data = [{'title': book.title, 'image_link': book.image_link} for book in books]
    return JsonResponse(wishlist_data, safe=False)

# Fungsi untuk menampilkan wishlist user
@login_required(login_url='/authentication/login/')
def show_wishlist(request):
    user = request.user

    # Fetch the wishlist data for the logged-in user
    wishlist_books = Wishlist.objects.filter(user=user).values('book')
    books = Book.objects.filter(pk__in=wishlist_books)

    wishlist_data = [{'title': book.title, 'image_link': book.image_link} for book in books]

    context = {
        'wishlist_data': wishlist_data,  # Pass the wishlist data to the template
        'name': request.user.username,
    }

    return render(request, "show_wishlist.html", context)


@register.filter(name='get_dict_value')
def get_dict_value(dictionary, key):
    return dictionary.get(key, 0)  # Return 0 if key is not found
        
# Fungsi untuk menampilkan inventory user
@login_required(login_url='/authentication/login/')       
def show_inventory(request):
    user = request.user
    inventory_books = Inventory.objects.filter(user=user)
    context = {
        'name': request.user.username,
        'inventory': inventory_books,
    }

    return render(request, "show_inventory.html", context)


