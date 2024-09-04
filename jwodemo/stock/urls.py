from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stock_home, name='stock_home'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('create_stock/', views.create_stock, name='create_stock'),
]
