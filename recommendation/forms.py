from django.forms import ModelForm
from .models import Recommendation

class RecommendationForm(ModelForm):
    class Meta:
        model = Recommendation
        fields = ['book_title',
                'another_book_title',
                'recommendation_scale',
                'description']