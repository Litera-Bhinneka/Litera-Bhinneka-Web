from django.shortcuts import render
from catalog.models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers


# Create your views here.
def show_catalog(request):
    books = Book.objects.all().values()
    context = {
        'books': books,
        'name': request.user.username,
    }

    return render(request, "show_catalog.html", context)

def get_product_json(request):
    product_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        image_link = request.POST.get("image_link")  # Sesuaikan dengan nama yang dikirim dari form di template
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        year_of_published = request.POST.get("year_of_published")


        # Periksa apakah produk dengan judul yang sama sudah ada
        if Book.objects.filter(title=title).exists():
            response_data = {'error': 'Produk dengan judul yang sama sudah ada.'}
            return JsonResponse(response_data, status=400)  # Respons dengan status 400 (Bad Request)

        new_product = Book(image_link=image_link, title=title, author=author, category=category, year_of_published=year_of_published, rating=0)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
