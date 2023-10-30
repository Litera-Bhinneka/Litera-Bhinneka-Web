from django.contrib import admin
from catalog.models import Book

# Register your models here.
@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
   list_display=['title', 'rating', 'author', 'category', 
                 'image_link', 'publisher', 
                 'description', 'year_of_published']
