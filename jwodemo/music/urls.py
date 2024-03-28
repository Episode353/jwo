from django.urls import path
from . import views

urlpatterns = [
    path('music', views.music_items, name='music'),
    path('album/<slug:slug>/', views.album, name='album'),
    path('submit-recommendation/', views.submit_recommendation, name='submit_recommendation'),
]
