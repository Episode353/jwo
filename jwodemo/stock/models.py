from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

class Stock(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)  # Hex color picker
    value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.0'))
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ManyToManyField(User, through='StockOwnership', related_name='owned_stocks')

    def __str__(self):
        return self.name

class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, related_name='history', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for precision
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stock.name} at {self.timestamp}: {self.price}"

class StockOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} owns {self.quantity} of {self.stock.name}'
