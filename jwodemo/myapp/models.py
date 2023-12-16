from django.db import models

# Create your models here.
class account(models.Model):
    # User's Name
    name = models.CharField(max_length=100)
    # How many Seep Coins someone can have
    coin_count = models.IntegerField()
    # Seep Coin Message
    coin_message = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name


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

# python manage.py makemigrations
# python manage.py migrate

