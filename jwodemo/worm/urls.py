# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='worm/main'),
    path('create_worm/', views.create_worm, name='create_worm'),
]
