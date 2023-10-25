from django.shortcuts import render, get_object_or_404
from review.models import Review
from catalog.models import Book
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


def see_book_review(request, id):
    book = get_object_or_404(Book, pk=id)
    reviews = Review.objects.filter(book_title=book.title)

    context = {
        'book': book,
        'reviews': reviews,
        'name': request.user.username,
    }

    return render(request, "book_review.html", context)


def add_review(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.reviewer_name = request.user.username 
        review.save()
        return HttpResponseRedirect(reverse('review:show_review'))

    context = {'form': form, 'name':request.user.username}
    return render(request, "add_review.html", context)