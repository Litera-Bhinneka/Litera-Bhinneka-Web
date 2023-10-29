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
        
        # widgets = {
        #     'out_book_title': forms.TextInput(attrs={
        #         'name':"out_book_title",
        #         'id':"modal-out_book_title",
        #         'class':"form-control",
        #         'placeholder':"Book Title"
        #     }),
        #     'another_out_book_title': forms.TextInput(attrs={
        #         'name':"another_out_book_title",
        #         'id':"modal-another_out_book_title",
        #         'class':"form-control",
        #         'placeholder':"Another Book Title"
        #     }),
        #     'out_description': forms.Textarea(attrs={
        #         'name':"out_description",
        #         'id':"modal-out_description",
        #         'class':"form-control",
        #         'placeholder':"Description"
        #     }),
        # }