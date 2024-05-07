from django.urls import path, include
from . import views
from .views import save_drawing, get_drawings
from django.conf import settings
from django.conf.urls.static import static
from .views import todo_view, move_up, move_down

urlpatterns = [
    path("", views.home, name="home"),
    path('', include("encyclopedia.urls")),
    path('', include("music.urls")),
    path("seepcoin", views.seepcoin, name="seepcoin"),
    path("board", views.board, name="board"),
    path("gallery", views.gallery, name="gallery"),
    path("blog", views.blog, name="blog"),
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
    path('move-up/<int:id>/', move_up, name='move_up'),
    path('move-down/<int:id>/', move_down, name='move_down'),
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
