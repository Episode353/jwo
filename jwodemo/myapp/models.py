from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

class SeepCoinTransaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coin_count = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    name = models.CharField(max_length=100, blank=True)
    coin_message = models.CharField(max_length=255, blank=True)

    bio = models.TextField(null=True, blank=True,)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    steam_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    discord_url = models.CharField(max_length=255, null=True, blank=True)

    def clean(self):
        super().clean()
        self._validate_url(self.website_url, 'website_url')
        self._validate_url(self.steam_url, 'steam_url')
        self._validate_url(self.twitter_url, 'twitter_url')
        self._validate_url(self.instagram_url, 'instagram_url')
        self._validate_url(self.discord_url, 'discord_url')

    def _validate_url(self, url, field_name):
        if url and not url.startswith('https://www.'):
            raise ValidationError({field_name: f"The URL must start with 'https://www.'"})

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('home')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.name = instance.username  # Set the name to the username
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


from django.db import models

from django.db import models


class foodreview(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    photo_link = models.CharField(max_length=100, blank=True)  # Keep this for static reviews
    cover_image = models.ImageField(upload_to='food_images/', null=True, blank=True)  # New field for dynamic reviews
    date = models.DateTimeField()
    is_dynamic = models.BooleanField(default=False)  # Determines if the review is dynamic

    # Dynamic fields
    food_score = models.IntegerField(null=True, blank=True)  # Change to IntegerField
    image1 = models.ImageField(upload_to='food_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='food_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='food_images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='food_images/', null=True, blank=True)
    image5 = models.ImageField(upload_to='food_images/', null=True, blank=True)
    would_sip = models.BooleanField(null=True, blank=True)
    bob_marley = models.BooleanField(null=True, blank=True)
    stop_train = models.BooleanField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.is_dynamic and self.cover_image:
            return self.cover_image.url
        return self.photo_link  # Use the old image URL if not dynamic



class todo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField()
    description = models.TextField(blank=True)  # Changed to TextField
    progress = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.name

from django.db import models
import random
import string

class RedeemCode(models.Model):
    code = models.CharField(max_length=8, unique=True)
    amount = models.PositiveIntegerField()
    was_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    @staticmethod
    def generate_random_code(length=8):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

# This is the model for the stuff that can appear on the homepage on specific days
class SeasonalContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
