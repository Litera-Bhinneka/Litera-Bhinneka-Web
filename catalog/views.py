from django.shortcuts import render
from catalog.models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q


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

# def search_products(request):
#     query = request.GET.get('query', '')  # Ambil kata kunci pencarian dari parameter URL

#     # Lakukan pencarian berdasarkan judul, kategori, dan penulis
#     books = Book.objects.filter(
#         Q(title__icontains=query) | Q(category__icontains=query) | Q(author__icontains=query)
#     )

#     context = {
#         'books': books,
#         'name': request.user.username,
#     }

#     return render(request, "search_catalog.html", context)

# def search_products(request):
#     if request.method == 'GET':
#         category = request.GET.get("category")
#         products = Book.objects.filter(category__icontains=category).values()
#         return JsonResponse({'products': list(products)})
#     return HttpResponseNotFound()

# def search_products(request):
#     if request.method == 'GET':
#         category = request.GET.get("category")
#         print("Category:", category)  # Tambahkan ini untuk debugging
#         if category:
#             products = Book.objects.filter(category__icontains=category).values()
#             return JsonResponse({'products': list(products)})
#         else:
#             # Handle ketika parameter "category" tidak diberikan
#             return JsonResponse({'products': []})
#     return HttpResponseNotFound()

# def search_products(request):
#     if request.method == 'GET':
#         query = request.GET.get("query")  # Mengambil kata kunci pencarian dari parameter "query"
#         print("Query:", query)  # Debugging: Tampilkan query yang digunakan

#         if query:
#             # Lakukan pencarian berdasarkan judul
#             products = Book.objects.filter(title__icontains=query).values()
#             return JsonResponse({'products': list(products)})
#         else:
#             # Handle ketika parameter "query" tidak diberikan
#             return JsonResponse({'products': []})
#     return HttpResponseNotFound()

# def search_books(request):
#     query = request.GET.get('query', '')  # Mengambil judul buku dari parameter URL
#     books = Book.objects.filter(title__icontains=query)  # Melakukan pencarian berdasarkan judul
#     context = {
#         'books': books,
#         'query': query,
#     }
#     return render(request, 'search_books.html', context)

# def search_products(request):
#     if request.method == 'GET':
#         query = request.GET.get("query")  # Mengambil kata kunci pencarian dari parameter "query"

#         if query:
#             # Lakukan pencarian berdasarkan judul
#             products = Book.objects.filter(title__icontains=query)
#             return render(request, "search_results.html", {'products': products, 'query': query})
#         else:
#             # Handle ketika parameter "query" tidak diberikan
#             return render(request, "search_results.html", {'products': None, 'query': query})
#     return HttpResponseNotFound()

# def search_products(request):
#     if request.method == 'GET':
#         query = request.GET.get("query", "")

#         if query:
#             # Lakukan pencarian berdasarkan judul yang mengandung kata kunci pencarian
#             products = Book.objects.filter(Q(title__icontains=query))
#             return render(request, "search_results.html", {'products': products, 'query': query})
#         else:
#             # Handle ketika parameter "query" tidak diberikan
#             return render(request, "search_results.html", {'products': None, 'query': query})
#     return HttpResponseNotFound()

def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        if query:
            # Menggunakan Q objects untuk mencari judul buku yang cocok atau berisi query
            books = Book.objects.filter(
                Q(title__icontains=query) | Q(category__icontains=query) | Q(author__icontains=query) | Q(year_of_published__icontains=query)
            )
        else:
            books = Book.objects.all()

        # Ubah hasil pencarian menjadi data JSON
        book_list = [{'pk': book.pk, 'image_link': book.image_link, 'title': book.title, 'author': book.author, 'category': book.category, 'year_of_published': book.year_of_published} for book in books]

        return JsonResponse({'books': book_list})
    else:
        return JsonResponse({'error': 'Metode permintaan tidak valid'}, status=400)



# def search_books(request):
#     query = request.GET.get('query', '')
#     author = request.GET.get('author', '')
#     title = request.GET.get('title', '')
#     category = request.GET.get('category', '')

#     # Gunakan operator Q untuk menggabungkan beberapa kriteria pencarian
#     books = YourBookModel.objects.filter(
#         Q(author__icontains=author) |
#         Q(title__icontains=title) |
#         Q(category__icontains=category) |
#         Q(some_other_field__icontains=query)
#     )

#     # Buat respons JSON dengan buku-buku yang cocok
#     books_data = [{'pk': book.pk, 'image_link': book.image_link, 'title': book.title, 'author': book.author, 'category': book.category, 'year_of_published': book.year_of_published} for book in books]

#     return JsonResponse({'books': books_data})
