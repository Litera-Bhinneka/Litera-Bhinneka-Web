from django.db import models
from catalog.models import Book
from django.contrib.auth.models import User

# Create your models here.
class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)