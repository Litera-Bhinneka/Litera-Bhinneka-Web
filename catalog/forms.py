from django import forms
from .models import Book

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'year_of_published', 'description', 'image_link'] 
