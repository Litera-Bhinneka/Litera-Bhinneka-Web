from django.forms import ModelForm
from review.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['book_title',
                'review_score',
                'review_summary',
                'review_text']