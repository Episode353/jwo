# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stock_home, name='stock_home'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('create_stock/', views.create_stock, name='create_stock'),
    path('stock/<int:stock_id>/buy/', views.buy_stock, name='buy_stock'),
    path('stock/<int:stock_id>/sell/', views.sell_stock, name='sell_stock'),
]
