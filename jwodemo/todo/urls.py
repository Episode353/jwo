from django.urls import path
from . import views

urlpatterns = [
    path('tree-todo/', views.tree_todo_view, name='tree_todo_view'),
    path('tree-todo/add-child/', views.add_child, name='add_child'),
    path('tree-todo/delete-item/', views.delete_item, name='delete_item'),
    path('tree-todo/rename-item/', views.rename_item, name='rename_item'),
    path('tree-todo/toggle-item/', views.toggle_item, name='toggle_item'),
    path('tree-todo/poll-tree/', views.poll_tree, name='poll_tree'),
    path('tree-todo/move-item-up/', views.move_item_up, name='move_item_up'),       # New
    path('tree-todo/move-item-down/', views.move_item_down, name='move_item_down'), # New
]
