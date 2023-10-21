from django.db import models

# Create your models here.
class Review(models.Model):
    book_title = models.CharField(max_length=255)
    reviewer_name = models.CharField(max_length=150)
    review_score = models.IntegerField()
    review_summary = models.CharField(max_length=255)
    review_text = models.TextField() 
    review_date = models.DateTimeField(auto_now_add=True)
