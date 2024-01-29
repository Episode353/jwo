from django.urls import path

from . import views

urlpatterns = [
    path("jworld/", views.index, name="jworld"),
    path("jworld/wiki/<str:title>", views.entry, name="entry"),
    path("jworld/search/", views.search, name="search"),
    path("jworld/new/", views.new_page, name="new_page"),
    path("jworld/edit/", views.edit, name="edit"),
    path("jworld/save_edit/", views.save_edit, name="save_edit"),
    path("jworld/rand/", views.rand, name="rand"),
    path('jworld/delete/', views.delete, name='delete'),
]
