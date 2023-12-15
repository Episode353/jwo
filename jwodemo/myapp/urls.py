from django.urls import path
from . import views

urlpatterns=[
    path("", views.home, name="home"),
    path("seepcoin", views.seepcoin, name="seepcoin"),
    path("board", views.board, name="board"),
    path("blog", views.blog, name="blog"),
    path("food", views.foodpage, name="foodpage"),
    path("food/<slug:slug>/", views.food_ar, name="food_ar"),
]