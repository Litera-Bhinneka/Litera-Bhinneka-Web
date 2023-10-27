from django.shortcuts import render
from .models import Recommendation
from catalog.models import Book
from manage_user.models import Inventory
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from .forms import RecommendationForm
from django.core import serializers
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_recommendation(request):
    recommendations = Recommendation.objects.all().values()
    context = {
        'recommendations': recommendations,
        'name': request.user.username
    }
    return render(request, 'show_recommendation.html', context)

def add_recommendation(request):
    form = RecommendationForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        recommendation = form.save(commit=False)
        recommendation.recommender_name = request.user.username 
        recommendation.save()
        return HttpResponseRedirect(reverse('recommendation:show_recommendation'))

    context = {'form': form}
    return render(request, "add_recommendation.html", context)

@csrf_exempt
def add_recommendation_ajax(request, bookId1, bookId2):
    if request.method == 'POST':
        recommender_name = request.user.username
        description = request.POST.get("description_text")
        book_title1 = get_object_or_404(Book, pk=bookId1).title
        book_title2 = get_object_or_404(Book, pk=bookId2).title
        print(bookId1)
        print(bookId2)
        new_product = Recommendation(book_title=book_title1, another_book_title=book_title2, description=description, recommendation_scale=0, recommender_name=recommender_name)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_user_inventory_json(request):
    user = request.user
    inventory = Inventory.objects.filter(user=user)
    book_title = []
    for i in inventory:
        book_title.append(i.book.title)
    return JsonResponse({'book_titles': book_title})

def get_book_image(request):
    user = request.user
    inventory = Inventory.objects.filter(user=user)
    book_image = []
    for i in inventory:
        book_image.append(i.book.image_link)
    return JsonResponse({'book_images': book_image})

def get_book_ids(request):
    user = request.user
    inventory = Inventory.objects.filter(user=user)
    book_ids = []
    for i in inventory:
        book_ids.append(i.book.id)
    return JsonResponse({'book_ids': book_ids})

def get_recommendation_json(request):
    rec = Recommendation.objects.all()
    return HttpResponse(serializers.serialize('json', rec))