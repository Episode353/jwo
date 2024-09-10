from django.urls import path, include
from . import views
from .views import save_drawing, get_drawings
from django.conf import settings
from django.conf.urls.static import static
from .views import todo_view, redeem_code_form

from django.conf.urls import handler404
from .views import custom_404_view, redeem_code

handler404 = custom_404_view

urlpatterns = [
    path("", views.home, name="home"),
    path('', include("music.urls")),
    path('stock/', include("stock.urls")),
    path('blog/', include("blog.urls")),
    path("seepcoin", views.seepcoin, name="seepcoin"),
    path("board", views.board, name="board"),
    path("gallery", views.gallery, name="gallery"),
    path("food", views.foodpage, name="foodpage"),
    path("food/<slug:slug>/", views.food_ar, name="food_ar"),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path("trade-seep-coins", views.trade_seep_coins, name="trade_seep_coins"),
    path('edit_coin_message/', views.edit_coin_message, name='edit_coin_message'),
    path('save_drawing/', save_drawing, name='save_drawing'),
    path('get_drawings/', get_drawings, name='get_drawings'),
    path("tool", views.tool, name="tool"),
    path("translator", views.translator, name="translator"),
    path("map", views.mapdirect, name="mapdirect"),
    path("todo", views.todo_view, name="todo"),
    path('worm/', include('worm.urls')),
    path("timenow", views.timenow, name="timenow"),
    path('members/redeem/<str:code>/', redeem_code, name='redeem_code'),
    path('members/redeem/', redeem_code_form, name='redeem_code_form'),
    path('ckeditor/', include('ckeditor_uploader.urls'))
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
