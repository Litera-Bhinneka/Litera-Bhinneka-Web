from django.db import models

# Create your models here.
class Recommendation(models.Model):
    book_title = models.CharField(max_length=255)
    another_book_title = models.CharField(max_length=255)
    book_image = models.URLField()
    another_book_image = models.URLField()
    recommender_name = models.CharField(max_length=150)
    recommendation_scale = models.IntegerField()
    description = models.TextField()
    recommendation_date = models.DateTimeField(auto_now_add=True)