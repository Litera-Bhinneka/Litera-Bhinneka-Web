from django.forms import ModelForm
from .models import Recommendation

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