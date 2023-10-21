from django.shortcuts import render
from review.models import Review
from django.http import HttpResponseRedirect
from review.forms import ReviewForm
from django.urls import reverse

# Create your views here.
def show_review(request):
    reviews = Review.objects.all().values()
    context = {
        'reviews': reviews,
    }

    return render(request, "show_review.html", context)


def add_review(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.reviewer_name = request.user.username 
        review.save()
        return HttpResponseRedirect(reverse('review:show_review'))

    context = {'form': form}
    return render(request, "add_review.html", context)