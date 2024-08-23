from django.contrib import admin
from .models import Post, Category, BlogProfile, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(BlogProfile)
admin.site.register(Comment)