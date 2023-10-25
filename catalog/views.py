from django.shortcuts import render
from catalog.models import Book

# Create your views here.
def show_catalog(request):
    books = Book.objects.all().values()
    context = {
        'books': books,
        'name': request.user.username,
    }

    return render(request, "show_catalog.html", context)