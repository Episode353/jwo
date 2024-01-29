from django.contrib import admin
from .models import foodreview, Profile, SeepCoinTransaction

# Register your models here.
admin.site.register(foodreview)
admin.site.register(Profile)
admin.site.register(SeepCoinTransaction)
