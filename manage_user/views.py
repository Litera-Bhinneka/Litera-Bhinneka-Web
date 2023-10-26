from django.shortcuts import render, get_object_or_404
from catalog.models import Book
from manage_user.models import Inventory
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
