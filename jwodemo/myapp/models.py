from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class SeepCoinTransaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coin_count = models.IntegerField(default=0)
    name = models.CharField(max_length=100, blank=True)
    coin_message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username  # Set the default name to the usernamee

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.name = instance.username  # Set the name to the username
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class foodreview(models.Model):
    # Name of the Food Review
    name = models.CharField(max_length=100)
    # Link to Food Review
    slug = models.CharField(max_length=100)
    # Food Review Image
    PhotoLink = models.CharField(max_length=100)
    # The Order in which to Display the Food Reviews
    # 0 being the first, and 9999 being the last
    Date = models.DateTimeField()

    def __str__(self):
        return self.name
    
class todo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField()
    description = models.TextField(blank=True)  # Changed to TextField
    progress = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.name