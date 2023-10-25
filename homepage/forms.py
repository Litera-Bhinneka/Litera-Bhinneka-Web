from django.forms import ModelForm
from homepage.models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback'].widget.attrs.update({
            'placeholder': 'Enter your question here',
            'cols' : '20',
            'rows' : '5',
        })