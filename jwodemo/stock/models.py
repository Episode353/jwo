from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)
    color = models.CharField(max_length=7, default='#007bff')  # Default color
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allow null

    def __str__(self):
        return self.name



class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, related_name='history', on_delete=models.CASCADE)
    price = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stock.name} at {self.timestamp}: {self.price}"
