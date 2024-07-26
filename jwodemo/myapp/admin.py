from django.contrib import admin
from .models import foodreview, Profile, SeepCoinTransaction, todo, RedeemCode
from music.models import Album, Song, Recommendation
from worm.models import Worm

# Register your models here.
admin.site.register(foodreview)
admin.site.register(Profile)
admin.site.register(SeepCoinTransaction)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Recommendation)
admin.site.register(todo)

from django.contrib import admin
from .models import RedeemCode

class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'was_used')
    readonly_fields = ('code',)

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = RedeemCode.generate_random_code()
        super().save_model(request, obj, form, change)

admin.site.register(RedeemCode, RedeemCodeAdmin)
