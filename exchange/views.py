from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from manage_user.models import Inventory
from exchange.models import Offer, Meet
from exchange.forms import MeetForm
from catalog.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

# Create your views here.
def show_books(request):
    search_query = request.GET.get('q', '')

    if search_query:
        books = Book.objects.filter(Q(title__icontains=search_query)).values()
    else:
        books = Book.objects.all().values()

    context = {
        'books': books,
        'name': request.user.username,
        'isadmin' : request.user.is_superuser,
        'query' : search_query,
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

@csrf_exempt
def accept_offer_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        offer = Offer.objects.get(id=data['id'])
        user1 = get_object_or_404(User, username=offer.Username1)
        user2 = get_object_or_404(User, username=offer.Username2)
        inventory1_data = json.loads(offer.Inventory1)
        inventory2_data = json.loads(offer.Inventory2)
        inventories = []
        
        for item in inventory1_data:
            try:
                book = Book.objects.get(id=item['book_id'])
                inventory1 = Inventory.objects.get(book=book, user=user1)
                amount = item['quantity']
            except Book.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "The specified book is not found.", "status": 404}, status=404)
            except Inventory.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "Inventory not found for the specified book and user.", "status": 404}, status=404)
            if amount == 0:
                continue
            elif amount > inventory1.amount:
                clean_inventories()
                return JsonResponse({"message": "The requested amount exceeds available inventory", "status": 403}, status=403)
            inventory2 = Inventory.objects.get_or_create(user=user2, book=book, defaults={"amount": 0})[0]
            inventory1.amount -= amount
            inventory2.amount += amount
            inventories.append(inventory2)
            if inventory1.amount == 0:
                inventory1.delete()
            else:
                inventories.append(inventory1)
        
        for item in inventory2_data:
            try:
                book = Book.objects.get(id=item['book_id'])
                inventory2 = Inventory.objects.get(book=book, user=user2)
                amount = item['quantity']
            except Book.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "The specified book is not found.", "status": 404}, status=404)
            except Inventory.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "Inventory not found for the specified book and user.", "status": 404}, status=404)
            if amount == 0:
                continue
            elif amount > inventory2.amount:
                clean_inventories()
                return JsonResponse({"message": "The requested amount exceeds available inventory", "status": 403}, status=403)
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
        return JsonResponse({"message": "Exchange successful. Your Inventory has been updated", "status": 200}, status=200)
    return JsonResponse({"message": "Invalid request method", "status": 400}, status=400)

@csrf_exempt
def delete_offer_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            offer = Offer.objects.get(id=data['id'])
            offer.delete()
            return JsonResponse({"message": "Successfully removed the Offer", "status": 200}, status=200)
        except Offer.DoesNotExist:
            return JsonResponse({"message": "Offer does not exist", "status": 404}, status=404)
    return JsonResponse({"message": "Invalid request method", "status": 400}, status=400)

@csrf_exempt
def create_offer_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        books1 = data['book1']
        books2 = data['book2']

        inventory1, inventory2 = [], []

        for book in books1:
            inventory1.append({'book_id': book['id'], 'quantity': book['amount'], 'book_title': book['title']})
        for book in books2:
            inventory2.append({'book_id': book['id'], 'quantity': book['amount'], 'book_title': book['title']})

        print(inventory1)
        print(inventory2)

        # Create an instance of the Offer model and populate its fields
        offer = Offer(
            Username1=data['username1'],
            Username2=data['username2'],
            Inventory1=json.dumps(inventory1),  # Serialize as JSON
            Inventory2=json.dumps(inventory2),  # Serialize as JSON
        )

        # Save the offer to the database
        offer.save()

        return JsonResponse({"status": "success"}, status=201)

    return JsonResponse({"status": "failed"}, status=404)

@csrf_exempt
def get_inventories_flutter(request, username1, username2):
    user = User.objects.get(username=username1)
    target = User.objects.get(username=username2)

    inventory_items1 = Inventory.objects.filter(user=user)
    inventory_items2 = Inventory.objects.filter(user=target)

    result1, result2 = [], []

    for inventory in inventory_items1:
        actual_book = inventory.book
        result = {
            'id': actual_book.pk,
            'title': actual_book.title,
            'image': actual_book.image_link,
            'amount': inventory.amount,
        }
        result1.append(result)

    for inventory in inventory_items2:
        actual_book = inventory.book
        result = {
            'id': actual_book.pk,
            'title': actual_book.title,
            'image': actual_book.image_link,
            'amount': inventory.amount,
        }
        result2.append(result)

    result = {
        'user': result1,
        'target': result2,
    }

    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def get_owners_flutter(request, id, username):
    book = get_object_or_404(Book, id=id)  # Retrieve the book
    print(request.user)
    # Exclude the user who made the request and filter users from inventories
    users = User.objects.exclude(username=username).filter(Q(inventory__book=book)).distinct()
    json_data = serializers.serialize('json', users, fields=('username', 'pk'))
    return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def get_offers_flutter(request, username):
    user = User.objects.get(username=username)
    if (user.is_superuser):
        return HttpResponse(json.dumps({'sent:': [], 'received': json.loads(serializers.serialize('json', Offer.objects.all(), fields=('Username1, Username2')))}), content_type='application/json')
    
    offers_sent = Offer.objects.filter(Username2=username)
    offers_sent_json = serializers.serialize('json', offers_sent, fields=('Username1, Username2'))
    offers_received = Offer.objects.filter(Username1=username)
    offers_received_json = serializers.serialize('json', offers_received, fields=('Username1, Username2'))

    offers = {
        'sent': json.loads(offers_sent_json),
        'received': json.loads(offers_received_json),
    }
    return HttpResponse(json.dumps(offers), content_type='application/json')

@csrf_exempt
def detail_offer_flutter(request, id):
    offer = get_object_or_404(Offer, pk=id)
    inventory1 = json.loads(offer.Inventory1)
    inventory2 = json.loads(offer.Inventory2)

    result1, result2 = [], []

    for book in inventory1:
        actual_book = get_object_or_404(Book, pk=book['book_id'])
        result = {
            'id': book['book_id'],
            'title': actual_book.title,
            'image': actual_book.image_link,
            'amount': book['quantity'],
        }
        result1.append(result)

    for book in inventory2:
        actual_book = get_object_or_404(Book, pk=book['book_id'])
        result = {
            'id': book['book_id'],
            'title': actual_book.title,
            'image': actual_book.image_link,
            'amount': book['quantity'],
        }
        result2.append(result)

    result = {
        'inventory1' : result1,
        'inventory2' : result2,
    }

    return HttpResponse(json.dumps(result), content_type='application/json')

def get_owners(request, id):
    book = get_object_or_404(Book, id=id)  # Retrieve the book
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
        book_titles = form_data.getlist('book_titles')  # Retrieve book Titles from the form data

        # Combine book IDs, quantities, and titles into dictionaries
        user1_inventory = [{'book_id': int(book_ids[i]), 'quantity': int(user1_item_quantities[i]), 'book_title': str(book_titles[i])}
                          for i in range(len(user1_item_quantities)) if int(user1_item_quantities[i]) > 0]
        user2_inventory = [{'book_id': int(book_ids[i + len(user1_item_quantities)]), 'quantity': int(user2_item_quantities[i]), 'book_title': str(book_titles[i + len(user1_item_quantities)])}
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

        return JsonResponse({"message": "CREATED", "id" : offer.pk}, status=201)

    return JsonResponse({"message": "Not Found"}, status=404)

@login_required(login_url='/authentication/login/')
def show_offers(request):
    if request.user.is_superuser:
        offers = Offer.objects.all()
        res = []
        for offer in offers:
            user1_items = json.loads(offer.Inventory1)
            user2_items = json.loads(offer.Inventory2)
            user1_name = offer.Username1
            user2_name = offer.Username2
            meet = Meet.objects.filter(offer=offer)
            if (len(meet) > 0):
                meet = meet[0]
            else:
                meet = False

            res.append({
                'user1_items': user1_items,
                'user2_items': user2_items,
                'user1_name': user1_name,
                'user2_name': user2_name,
                'id': offer.pk,
                'meet': meet,
            })
        
        context = {
            'offers': res,
            'name': request.user.username,
            'isadmin' : request.user.is_superuser,
        }

    else:
        offers_sent = Offer.objects.filter(Username2=request.user.username)
        offers_received = Offer.objects.filter(Username1=request.user.username)

        sent_offers = []
        received_offers = []

        for offer in offers_sent:
            user1_items = json.loads(offer.Inventory1)
            user2_items = json.loads(offer.Inventory2)
            user1_name = offer.Username1
            meet = Meet.objects.filter(offer=offer)
            if (len(meet) > 0):
                meet = meet[0]
            else:
                meet = False

            sent_offers.append({
                'user1_items': user1_items,
                'user2_items': user2_items,
                'user1_name': user1_name,
                'id': offer.pk,
                'meet': meet,
            })

        for offer in offers_received:
            user1_items = json.loads(offer.Inventory1)
            user2_items = json.loads(offer.Inventory2)
            user2_name = offer.Username2
            meet = Meet.objects.filter(offer=offer)
            if (len(meet) > 0):
                meet = meet[0]
            else:
                meet = False

            received_offers.append({    
                'user1_items': user1_items,
                'user2_items': user2_items,
                'user2_name': user2_name,
                'id': offer.pk,
                'meet': meet,
            })

        context = {
            'sent_offers': sent_offers,
            'received_offers': received_offers,
            'name': request.user.username,
            'isadmin' : request.user.is_superuser,
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
            try:
                book = Book.objects.get(id=item['book_id'])
                inventory1 = Inventory.objects.get(book=book, user=user1)
                amount = item['quantity']
            except Book.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "The specified book is not found."}, status=404)
            except Inventory.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "Inventory not found for the specified book and user."}, status=404)
            if amount == 0:
                continue
            elif amount > inventory1.amount:
                clean_inventories()
                return JsonResponse({"message": "The requested amount exceeds available inventory"}, status=403)
            inventory2 = Inventory.objects.get_or_create(user=user2, book=book, defaults={"amount": 0})[0]
            inventory1.amount -= amount
            inventory2.amount += amount
            inventories.append(inventory2)
            if inventory1.amount == 0:
                inventory1.delete()
            else:
                inventories.append(inventory1)
        
        for item in inventory2_data:
            try:
                book = Book.objects.get(id=item['book_id'])
                inventory2 = Inventory.objects.get(book=book, user=user2)
                amount = item['quantity']
            except Book.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "The specified book is not found."}, status=404)
            except Inventory.DoesNotExist:
                clean_inventories()
                offer.delete()
                return JsonResponse({"message": "Inventory not found for the specified book and user."}, status=404)
            if amount == 0:
                continue
            elif amount > inventory2.amount:
                clean_inventories()
                return JsonResponse({"message": "The requested amount exceeds available inventory"}, status=403)
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

@login_required(login_url='/authentication/login/')
def schedule_meet(request, id):
    if request.method == 'POST':
        form = MeetForm(request.POST)
        print(form)
        if form.is_valid():
            meet = form.save(commit=False)
            meet.sender = request.user
            meet.offer = Offer.objects.get(id=id)
            meet.receiver = User.objects.get(username=meet.offer.Username1)
            meet.save()
            return JsonResponse({"message": "Successfully Scheduled an Offline Meeting"}, status=201)
        else:
            return JsonResponse({"message": "Form is not valid!"}, status=400)
    else:
        form = MeetForm()
        context = {
            'name': request.user.username,
            'form': form,
            'id': id,
        }
    return render(request, "schedule_meet.html", context)

# Helper Function
def clean_inventories():
    inventories = Inventory.objects.all()
    for inventory in inventories:
        if inventory.amount == 0:
            inventory.delete()