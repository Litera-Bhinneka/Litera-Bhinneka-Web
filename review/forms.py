from django.forms import ModelForm
from review.models import Review
from django import forms

RATING_CHOICES = (
        ('5', 'rating5'),
        ('4', 'rating4'),
        ('3', 'rating3'),
        ('2', 'rating2'),
        ('1', 'rating1'),
    )

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['book_title',
                'review_score',
                'review_summary',
                'review_text']
        
        review_score = forms.ChoiceField(
            choices=RATING_CHOICES,
            widget=forms.RadioSelect(attrs={'class': 'hidden'}),
            required=True,
        )
        
        widgets = {
            'review_summary': forms.Textarea(attrs={
                'name':"review_summary",
                'id':"review_summary",
                'rows':"1",
                'class':"resize-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-800 focus:border-green-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white",
                'placeholder':"My new FAVORITE COOKBOOK!",
                'required': 'required', 
            }),
            'review_text': forms.Textarea(attrs={
                'name':"review_text",
                'id':"review",
                'rows':"6",
                'class':"resize-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-800 focus:border-green-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white",
                'placeholder':"I recently found out I have numerous food allergies and sensitivities - this cookbook is definitely my new favorite! Not only are there TONS of delicious REAL FOOD recipes - they don't seem to be super complicated or time consuming!",
                'required': 'required', 
                }),
        }

        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            for index, (value, label) in enumerate(self.fields['review_score'].choices):
                self.fields['review_score'].widget.choices[index] = (value, label, {'id': f'rating{value}', 
                                                                              'value': value,
                                                                              'name': 'rating'})

        def clean_review_score(self):
            review_score = self.cleaned_data.get('review_score')
            if review_score == '0':
                raise forms.ValidationError("Please select a valid review score.")
            return review_score