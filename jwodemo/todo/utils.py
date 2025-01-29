from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def group_required(group_name):
    """
    Decorator to restrict view access to users in a specific group.
    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this page.")
        return _wrapped_view
    return decorator
