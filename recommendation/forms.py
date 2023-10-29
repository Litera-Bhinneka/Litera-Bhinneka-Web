from django.forms import ModelForm
from .models import Recommendation
from .models import OutsideRecommendation
from django import forms

class RecommendationForm(ModelForm):
    class Meta:
        model = Recommendation
        fields = ['book_title',
                'another_book_title',
                'book_id',
                'another_book_id',
                'recommender_name',
                'recommendation_scale',
                'book_image',
                'another_book_image',
                'description']
        
class OutsideRecommendationForm(forms.ModelForm):
    class Meta:
        model = OutsideRecommendation
        fields = ['out_book_title',
                'another_out_book_title',
                'out_description',
                'out_recommender_name']
        
        widgets = {
            'out_book_title': forms.Textarea(attrs={
                'name':"out_book_title",
                'id':"out_book_title",
                'rows':"1",
                'class':"form-control resize-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-800 focus:border-green-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white",
                'placeholder':"Book Title",
                'required': 'required', 
            }),
            'another_out_book_title': forms.Textarea(attrs={
                'name':"another_out_book_title",
                'id':"another_out_book_title",
                'rows':"1",
                'class':"form-control resize-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-800 focus:border-green-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white",
                'placeholder':"Another Book Title",
                'required': 'required', 
            }),
            'out_description': forms.Textarea(attrs={
                'name':"out_description",
                'id':"out_description",
                'rows':"6",
                'class':"form-control resize-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-800 focus:border-green-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white",
                'placeholder':"Description",
                'required': 'required', 
            }),
        }