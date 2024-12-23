from django.db import models

from django.contrib.auth.models import User

class Bounty(models.Model):
    TIER_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
    ]
    objective = models.TextField()
    reward = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    tier = models.CharField(max_length=3, choices=TIER_CHOICES, default='I')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"Bounty: {self.objective} - Tier: {self.tier}"
