from django.urls import path
from . import views
from .views import edit_profile

urlpatterns=[
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('account', views.account, name="account"),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('coin_coint/', views.coin_coint, name='coin_coint'),
]