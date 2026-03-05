from functools import wraps
from core.rbac import check_permission


def rbac_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            check_permission(request.user, permission)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator