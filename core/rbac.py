from rest_framework.permissions import BasePermission
from core.permissions_matrix import ROLE_PERMISSIONS


class RBACPermission(BasePermission):
    """
    Permission class that checks if the user role
    has the required permission defined in ROLE_PERMISSIONS
    """

    required_permission = None

    def has_permission(self, request, view):

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get role name
        role_name = request.user.profile.role.name

        # Permissions allowed for that role
        allowed_permissions = ROLE_PERMISSIONS.get(role_name, [])

        # Permission required by the view
        required_permission = getattr(view, "required_permission", None)

        # If view does not define permission, allow
        if required_permission is None:
            return True

        return required_permission in allowed_permissions