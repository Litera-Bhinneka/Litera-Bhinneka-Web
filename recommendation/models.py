from django.db import models
from review.models import Review
# Create your models here.
class Recommendation(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    book_title = models.CharField(max_length=255)
    another_book_title = models.CharField(max_length=255)
    book_id = models.IntegerField()
    another_book_id = models.IntegerField()
    book_image = models.URLField()
    another_book_image = models.URLField()
    recommender_name = models.CharField(max_length=150)
    recommendation_scale = models.IntegerField()
    description = models.TextField()
    recommendation_date = models.DateTimeField(auto_now_add=True)

class OutsideRecommendation(models.Model):
    out_book_title = models.CharField(max_length=255)
    another_out_book_title = models.CharField(max_length=255)
    out_description = models.TextField()
    out_recommendation_date = models.DateTimeField(auto_now_add=True)
    out_recommender_name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.out_book_title)