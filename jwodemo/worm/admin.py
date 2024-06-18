from django.contrib import admin
from .models import Worm

class WormAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_alive', 'health', 'sleep', 'hunger', 'happiness', 'badge', 'created_at', 'updated_at', 'time_of_death']
    list_display_links = ['id', 'name']  # Specify which fields should be clickable to open the detail page
    fields = ['name', 'is_alive', 'health', 'sleep', 'hunger', 'happiness', 'badge', 'last_fed', 'last_slept', 'last_played', 'created_at', 'updated_at', 'time_of_death']
    readonly_fields = ['updated_at']

admin.site.register(Worm, WormAdmin)
