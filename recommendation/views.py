from django.shortcuts import render
from .models import Recommendation
from catalog.models import Book
from manage_user.models import Inventory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
def add_recommendation_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        user = request.user

        new_product = Recommendation(name=name, price=price, description=description, user=user)
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

def get_recommendation_json(request):
    rec = Recommendation.objects.all()
    return HttpResponse(serializers.serialize('json', rec))