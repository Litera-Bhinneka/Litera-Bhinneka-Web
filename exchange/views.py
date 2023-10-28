from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from manage_user.models import Inventory
from exchange.models import Offer
from catalog.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

# Create your views here.
@login_required(login_url='/authentication/login/')
def show_books(request):
    search_query = request.GET.get('q', '')

    if search_query:
        books = Book.objects.filter(Q(title__icontains=search_query)).values()
    else:
        books = Book.objects.all().values()

    context = {
        'books': books,
        'name': request.user.username,
    }

    return render(request, "show_owners.html", context)

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


def get_owners(request, id):
    book = get_object_or_404(Book, id=id)  # Retrieve the book (assuming it's a single object)
    # Exclude the user who made the request and filter users from inventories
    users = User.objects.exclude(username=request.user.username).filter(Q(inventory__book=book)).distinct()
    return HttpResponse(serializers.serialize("json", users))

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
                          for i in range(len(user1_item_quantities)) if int(user1_item_quantities[i]) > 0]
        user2_inventory = [{'book_id': int(book_ids[i + len(user1_item_quantities)]), 'quantity': int(user2_item_quantities[i])}
                          for i in range(len(user2_item_quantities)) if int(user2_item_quantities[i]) > 0]

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

    sent_offers = []
    received_offers = []

    for offer in offers_sent:
        user1_items = json.loads(offer.Inventory1)
        user2_items = json.loads(offer.Inventory2)
        user1_name = offer.Username1

        for item in user1_items:
            try:
                book = Book.objects.get(id=item['book_id'])
                item['book_title'] = book.title
            except Book.DoesNotExist:
                item['book_title'] = 'Book not Found'

        for item in user2_items:
            try:
                book = Book.objects.get(id=item['book_id'])
                item['book_title'] = book.title
            except Book.DoesNotExist:
                item['book_title'] = 'Book not Found'

        sent_offers.append({
            'user1_items': user1_items,
            'user2_items': user2_items,
            'user1_name': user1_name,
            'id': offer.pk,
        })

    for offer in offers_received:
        user1_items = json.loads(offer.Inventory1)
        user2_items = json.loads(offer.Inventory2)
        user2_name = offer.Username2

        for item in user1_items:
            try:
                book = Book.objects.get(id=item['book_id'])
                item['book_title'] = book.title
            except Book.DoesNotExist:
                item['book_title'] = 'Book not Found'

        for item in user2_items:
            try:
                book = Book.objects.get(id=item['book_id'])
                item['book_title'] = book.title
            except Book.DoesNotExist:
                item['book_title'] = 'Book not Found'

        received_offers.append({    
            'user1_items': user1_items,
            'user2_items': user2_items,
            'user2_name': user2_name,
            'id': offer.pk,
        })

    context = {
        'sent_offers': sent_offers,
        'received_offers': received_offers,
        'name': request.user.username,
    }

    return render(request, "show_offers.html", context)

@login_required(login_url='/authentication/login/')
def delete_offer(request, id):
    if request.method == 'POST':
        offer = Offer.objects.get(id=id)
        offer.delete()
        return JsonResponse({"message": "Successfully removed the Offer"}, status=200)
    return JsonResponse({"message": "Invalid request method"}, status=400)

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
            inventory2 = Inventory.objects.get_or_create(user=user2, book=book, defaults={"amount": 0})[0]
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
            inventory1 = Inventory.objects.get_or_create(user=user1, book=book, defaults={"amount": 0})[0]
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
        return JsonResponse({"message": "Exchange successful. Your Inventory has been updated"}, status=200)
    return JsonResponse({"message": "Invalid request method"}, status=400)