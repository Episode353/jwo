from django.urls import path
from . import views

urlpatterns = [
    path('bounties/', views.bounty_list, name='bounty_list'),
    path('create/', views.create_bounty, name='create_bounty'),
    path('<int:bounty_id>/edit/', views.edit_bounty, name='edit_bounty'),
    path('<int:bounty_id>/delete/', views.delete_bounty, name='delete_bounty'),
]
