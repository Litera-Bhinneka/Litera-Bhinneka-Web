from django.shortcuts import render
from .models import Recommendation
from catalog.models import Book
from django.http import HttpResponseRedirect
from .forms import RecommendationForm
from django.urls import reverse

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