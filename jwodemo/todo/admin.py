from django.contrib import admin
from .models import TodoItem

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_done', 'created_at')
    list_filter = ('parent', 'is_done')
    search_fields = ('name',)
