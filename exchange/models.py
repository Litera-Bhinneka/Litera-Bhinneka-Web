from django.db import models
from django.contrib.auth.models import User
from manage_user.models import Inventory

# Create your models here.
class Offer(models.Model):
    Username1 = models.CharField(max_length=255)
    Username2 = models.CharField(max_length=255)
    Inventory1 = models.JSONField()
    Inventory2 = models.JSONField()

class Meet(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_meets')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_meets')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=255)
    message = models.TextField()