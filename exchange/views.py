from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from manage_user.models import Inventory
from exchange.models import Offer
from catalog.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@login_required(login_url='/authentication/login/')
def show_users(request):
    users = User.objects.exclude(username=request.user.username)
    inventory_data = []

    for user in users:
        inventory_items = Inventory.objects.filter(user=user)
        inventory_data.append(inventory_items)

    context = {
        'users': users.values(),
        'name': request.user.username,
    }

    return render(request, "show_users.html", context)

@login_required(login_url='/authentication/login/')
def offer_user(request, username):
    user = get_object_or_404(User, username=username)
    inventory_items1 = Inventory.objects.filter(user=user)
    inventory_items2 = Inventory.objects.filter(user=request.user)
    context1 = {
        'user': user,
        'inventory_items': inventory_items1,
    }

    context2 = {
        'user': request.user,
        'inventory_items': inventory_items2,
    }

    context = {
        'user1': context1,
        'user2': context2,
        'name': request.user.username,
    }

    return render(request, 'offer_user.html', context)


def get_books(request, username):
    user = get_object_or_404(User, username=username)
    inventory_items = Inventory.objects.filter(user=user)

    return HttpResponse(serializers.serialize("json", inventory_items))

@csrf_exempt
def add_offer(request):
    if request.method == 'POST':
        form_data = request.POST
        # Access form fields by name
        user1_item_quantities = form_data.getlist('user1_item_quantities')
        user2_item_quantities = form_data.getlist('user2_item_quantities')
        book_ids = form_data.getlist('book_ids')  # Retrieve book IDs from the form data

        # Combine book IDs and quantities into dictionaries
        user1_inventory = [{'book_id': int(book_ids[i]), 'quantity': int(user1_item_quantities[i])}
                          for i in range(len(user1_item_quantities))]
        user2_inventory = [{'book_id': int(book_ids[i + len(user1_item_quantities)]), 'quantity': int(user2_item_quantities[i])}
                          for i in range(len(user2_item_quantities))]

        # Create an instance of the Offer model and populate its fields
        offer = Offer(
            Username1=form_data['target_user'],
            Username2=request.user.username,
            Inventory1=json.dumps(user1_inventory),  # Serialize as JSON
            Inventory2=json.dumps(user2_inventory),  # Serialize as JSON
        )

        # Save the offer to the database
        offer.save()

        return JsonResponse({"message": "CREATED"}, status=201)

    return JsonResponse({"message": "Not Found"}, status=404)

@login_required(login_url='/authentication/login/')
def show_offers(request):
    offers_sent = Offer.objects.filter(Username2=request.user.username)
    offers_received = Offer.objects.filter(Username1=request.user.username)

    context = {
        'sent': offers_sent,
        'received': offers_received,
        'name': request.user.username,
    }

    return render(request, "show_offers.html", context)

@login_required(login_url='/authentication/login/')
def delete_offer(request, id):
    if request.method == 'POST':
        offer = Offer.objects.get(id=id)
        offer.delete()
    return redirect('/')

@login_required(login_url='/authentication/login/')
def accept_offer(request, id):
    if request.method == 'POST':
        offer = Offer.objects.get(id=id)
        user1 = get_object_or_404(User, username=offer.Username1)
        user2 = get_object_or_404(User, username=offer.Username2)
        inventory1_data = json.loads(offer.Inventory1)
        inventory2_data = json.loads(offer.Inventory2)
        inventories = []
        
        for item in inventory1_data:
            book = get_object_or_404(Book, id=item['book_id'])
            amount = item['quantity']
            inventory1 = get_object_or_404(Inventory, book=book, user=user1)
            if amount == 0:
                continue
            elif amount > inventory1.amount:
                return JsonResponse({"message": "The requested amount exceeds available inventory"}, status=400)
            inventory2 = Inventory.objects.get_or_create(user=user2, book=book, amount=0)[0]
            inventory1.amount -= amount
            inventory2.amount += amount
            inventories.append(inventory2)
            if inventory1.amount == 0:
                inventory1.delete()
            else:
                inventories.append(inventory1)
        
        for item in inventory2_data:
            book = get_object_or_404(Book, id=item['book_id'])
            amount = item['quantity']
            inventory2 = get_object_or_404(Inventory, book=book, user=user2)
            if amount == 0:
                continue
            elif amount > inventory2.amount:
                return JsonResponse({"message": "The requested amount exceeds available inventory"}, status=400)
            inventory1 = Inventory.objects.get_or_create(user=user1, book=book, amount=0)[0]
            inventory1.amount += amount
            inventory2.amount -= amount
            inventories.append(inventory1)
            if inventory2.amount == 0:
                inventory2.delete()
            else:
                inventories.append(inventory2)
        
        for inventory in inventories:
            inventory.save()

        offer.delete()
        return JsonResponse({"message": "Offer accepted and processed"}, status=200)
    return JsonResponse({"message": "Invalid request method"}, status=400)