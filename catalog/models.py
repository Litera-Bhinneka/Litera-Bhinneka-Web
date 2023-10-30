from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    rating = models.IntegerField()
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    image_link = models.URLField()
    publisher = models.CharField(max_length=255)
    description = models.TextField()
    year_of_published = models.IntegerField()

