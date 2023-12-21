from django.urls import path, include
from . import views

urlpatterns=[
    path("", views.home, name="home"),
    path("seepcoin", views.seepcoin, name="seepcoin"),
    path("board", views.board, name="board"),
    path("blog", views.blog, name="blog"),
    path("food", views.foodpage, name="foodpage"),
    path("food/<slug:slug>/", views.food_ar, name="food_ar"),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path("trade-seep-coins", views.trade_seep_coins, name="trade_seep_coins"),
    path('edit_coin_message/', views.edit_coin_message, name='edit_coin_message'),

]