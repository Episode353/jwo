from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TodoItem
from .utils import group_required  # Import the decorator
# views.py
from django.db.models import Max
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TodoItem

@group_required("todo group")
def tree_todo_view(request):
    root_items = TodoItem.objects.filter(parent__isnull=True).order_by('order')  # Changed from 'created_at' to 'order'

    # Calculate the latest update time among all TodoItems
    latest_update = TodoItem.objects.aggregate(max_time=Max('updated_at'))['max_time']

    # If there are no items, set some default (like now or None)
    if not latest_update:
        latest_update = timezone.now()

    context = {
        'root_items': root_items,
        'latest_update': latest_update.isoformat()  # pass as string
    }
    return render(request, 'tree_todo.html', context)


@group_required("todo group")
@require_http_methods(["POST"])
def add_child(request):
    """
    AJAX endpoint to add a child item to a given parent.
    Expects 'parent_id' and 'name' in POST data.
    If 'parent_id' is null (or missing), it means add a root item.
    """
    parent_id = request.POST.get('parent_id')
    name = request.POST.get('name', 'New Item')

    if parent_id:
        parent = get_object_or_404(TodoItem, id=parent_id)
        siblings = TodoItem.objects.filter(parent=parent).order_by('-order')
    else:
        # Add as a root item if no parent_id is provided
        siblings = TodoItem.objects.filter(parent__isnull=True).order_by('-order')

    last_order = siblings.first().order if siblings.exists() else 0
    new_order = last_order + 1

    if parent_id:
        child = TodoItem.objects.create(name=name, parent=parent, order=new_order)
    else:
        # Add as a root item if no parent_id is provided
        child = TodoItem.objects.create(name=name, order=new_order)

    return JsonResponse({
        'status': 'success',
        'id': child.id,
        'name': child.name,
        'parent_id': parent_id,
        'is_done': child.is_done,
        'order': child.order,  # Include 'order'
    })

@group_required("todo group")
@require_http_methods(["POST"])
def delete_item(request):
    """
    AJAX endpoint to delete an item (and all its children).
    Expects 'item_id' in POST data.
    """
    item_id = request.POST.get('item_id')
    item = get_object_or_404(TodoItem, id=item_id)
    item.delete()
    return JsonResponse({'status': 'success'})

@group_required("todo group")
@require_http_methods(["POST"])
def rename_item(request):
    """
    AJAX endpoint to rename an item.
    Expects 'item_id' and 'new_name' in POST data.
    """
    item_id = request.POST.get('item_id')
    new_name = request.POST.get('new_name')
    item = get_object_or_404(TodoItem, id=item_id)
    item.name = new_name
    item.save()
    return JsonResponse({'status': 'success', 'new_name': new_name})

@group_required("todo group")
@require_http_methods(["POST"])
def toggle_item(request):
    """
    AJAX endpoint to toggle the 'is_done' status of an item.
    Expects 'item_id' in POST data.
    """
    item_id = request.POST.get('item_id')
    item = get_object_or_404(TodoItem, id=item_id)
    item.is_done = not item.is_done
    item.save()
    return JsonResponse({'status': 'success', 'is_done': item.is_done})

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import TodoItem

@group_required("todo group")
@require_GET
def poll_tree(request):
    """
    Returns JSON data representing the entire tree (all items).
    """
    # Query all items
    items = TodoItem.objects.all().select_related('parent').order_by('order')  # Ensure ordering by 'order'

    # Convert them into a structure that’s easy to re-render
    data = []
    for item in items:
        data.append({
            'id': item.id,
            'name': item.name,
            'parent_id': item.parent.id if item.parent else None,
            'is_done': item.is_done,
            'order': item.order,  # Include 'order'
        })

    return JsonResponse({'items': data})


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TodoItem

# Existing imports and views...
@group_required("todo group")
@require_http_methods(["POST"])
def move_item_up(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(TodoItem, id=item_id)

    if item.parent:
        siblings = list(TodoItem.objects.filter(parent=item.parent).order_by('order'))
    else:
        siblings = list(TodoItem.objects.filter(parent__isnull=True).order_by('order'))

    index = siblings.index(item)
    if index > 0:
        previous_item = siblings[index - 1]
        # Swap the 'order' values
        item.order, previous_item.order = previous_item.order, item.order
        item.save()
        previous_item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Already the first item.'})
    
@group_required("todo group")
@require_http_methods(["POST"])
def move_item_down(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(TodoItem, id=item_id)

    if item.parent:
        siblings = list(TodoItem.objects.filter(parent=item.parent).order_by('order'))
    else:
        siblings = list(TodoItem.objects.filter(parent__isnull=True).order_by('order'))

    index = siblings.index(item)
    if index < len(siblings) - 1:
        next_item = siblings[index + 1]
        # Swap the 'order' values
        item.order, next_item.order = next_item.order, item.order
        item.save()
        next_item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Already the last item.'})
