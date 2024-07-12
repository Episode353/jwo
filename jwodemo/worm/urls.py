# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('revive/<str:worm_name>', views.revive, name='revive'),
    path('', views.main, name='worm/main'),
    path('create_worm/', views.create_worm, name='create_worm'),
    path('feed/', views.worm_feed, name='worm_feed'),
    path('play/', views.worm_play, name='worm_play'),
    path('sleep/', views.worm_sleep, name='worm_sleep'),
    path('graveyard/', views.graveyard, name='graveyard'),
]
