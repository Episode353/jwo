from django.contrib import admin
from .models import Stock, StockHistory, StockOwnership

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'last_updated']

@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ['stock', 'price', 'timestamp']  # Include timestamp here

admin.site.register(StockOwnership)
# If you prefer not to use the @admin.register decorator
# admin.site.register(Stock)
# admin.site.register(StockHistory, StockHistoryAdmin)
