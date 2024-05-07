from django.contrib import admin
from .models import foodreview, Profile, SeepCoinTransaction, todo
from music.models import Album, Song, Recommendation

# Register your models here.
admin.site.register(foodreview)
admin.site.register(Profile)
admin.site.register(SeepCoinTransaction)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Recommendation)
admin.site.register(todo)
