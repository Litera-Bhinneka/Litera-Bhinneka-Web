from django.shortcuts import render
from .models import Recommendation
from catalog.models import Book
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RecommendationForm
from django.core import serializers
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

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

def find_book_id(request, book_name):
    book = get_object_or_404(Book, title=book_name)

    return redirect('review:book_review', id=book.id)

def get_recommendation_json(request):
    rec = Recommendation.objects.all()
    return HttpResponse(serializers.serialize('json', rec))