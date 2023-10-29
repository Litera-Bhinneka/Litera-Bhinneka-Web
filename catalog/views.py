from django.shortcuts import render
from catalog.models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from review.management.commands.load_rating_data import Command
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookEditForm


# Create your views here.
def show_catalog(request):
    books = Book.objects.all().values()
    context = {
        'books': books,
        'name': request.user.username,
    }
    Command().handle()

    return render(request, "show_catalog.html", context)

def get_product_json(request):
    product_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        image_link = request.POST.get("image_link") 
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        year_of_published = request.POST.get("year_of_published")

        if Book.objects.filter(title=title).exists():
            response_data = {'error': 'Produk dengan judul yang sama sudah ada.'}
            return JsonResponse(response_data, status=400)  

        new_product = Book(image_link=image_link, title=title, author=author, category=category, year_of_published=year_of_published, rating=0)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) | Q(category__icontains=query) | Q(author__icontains=query) | Q(year_of_published__icontains=query)
            )
        else:
            books = Book.objects.all()

        book_list = [{'pk': book.pk, 'image_link': book.image_link, 'title': book.title, 'author': book.author, 'category': book.category, 'year_of_published': book.year_of_published} for book in books]

        return JsonResponse({'books': book_list})
    else:
        return JsonResponse({'error': 'Metode permintaan tidak valid'}, status=400) 

def edit_book(request, id):
    # Get product berdasarkan ID
    product = Book.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = BookEditForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return redirect('catalog:show_catalog')

    context = {'form': form, 'name': request.user.username,}
    return render(request, "edit_book.html", context)