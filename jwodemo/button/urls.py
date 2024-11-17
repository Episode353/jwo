from django.urls import path
from . import views

urlpatterns = [
    path('button-frontend/', views.button_frontend, name='button_frontend'),
    path('button-backend/', views.button_backend, name='button_backend'),
    path('get-updates/', views.get_updates, name='get_updates'),
    path('clear-updates/', views.clear_updates, name='clear_updates'),
]
