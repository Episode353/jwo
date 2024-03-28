from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album_art = models.CharField(max_length=100)

    release_date = models.CharField(max_length=4)

    hours = models.CharField(max_length=3)
    minutes = models.CharField(max_length=3)

    length = models.DurationField()
    slug = models.CharField(max_length=100)

    review_body = models.TextField()

    def __str__(self):
        return self.name

class Song(models.Model):
    TIER_CHOICES = [
        ('S', 'S'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=1, choices=TIER_CHOICES)

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    recommendation_text = models.TextField()

    def __str__(self):
        return self.recommendation_text
