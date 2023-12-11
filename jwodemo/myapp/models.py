from django.db import models

# Create your models here.
class account(models.Model):
    # User's Name
    name = models.CharField(max_length=100)
    # How many Seep Coins someone can have
    coin_count = models.IntegerField()
    # Seep Coin Message
    coin_message = models.TextField()


    def __str__(self):
        return self.name


# python manage.py makemigrations
# python manage.py migrate

