from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from manage_user.models import Inventory
from catalog.models import Book
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='/authentication/login/')
def show_users(request):
    users = User.objects.all()
    inventory_data = []

    for user in users:
        inventory_items = Inventory.objects.filter(user=user)
        inventory_data.append(inventory_items)

    context = {
        'users': users.values(),
        'name': request.user.username,
        'inventory_data': inventory_data,
    }

    return render(request, "show_users.html", context)

@login_required(login_url='/authentication/login/')
def offer_user(request, username):
    user = get_object_or_404(User, username=username)
    inventory_items1 = Inventory.objects.filter(user=user)
    inventory_items2 = Inventory.objects.filter(user=request.user)

    books1 = []
    books2 = []
    amounts1 = []
    amounts2 = []

    for item in inventory_items1:
        books1.append(item.book)
        amounts1.append(item.amount)
    
    for item in inventory_items2:
        books1.append(item.book)
        amounts1.append(item.amount)

    context1 = {
        'user': user,
        'inventory_items': inventory_items1,
        'books': books1,
        'amounts': amounts1,
    }

    context2 = {
        'user': request.user,
        'inventory_items': inventory_items2,
        'books': books2,
        'amounts': amounts2,
    }

    context = {
        'user1': context1,
        'user2': context2,
    }

    return render(request, 'offer_user.html', context)


def get_books(request, username):
    user = get_object_or_404(User, username=username)
    inventory_items = Inventory.objects.filter(user=user)

    books = []

    for item in inventory_items:
        books.append(item.book)

    context = {
        'user': user,
        'inventory_items': inventory_items,
        'books': books,
    }

    return HttpResponse(serializers.serialize("json", context))