from rest_framework import permissions

from roles.models import RoleChoices


class IsAdministrator(permissions.BasePermission):
    """
    Administrator Based Permissions with Roles
    """
    def has_permission(self, request, view):
        # Access the current user and check if they are Administrators

        if request.method in permissions.SAFE_METHODS:
            return True

        role = request.user.profile.role

        # check if the user is ADMIN
        if role.name == RoleChoices.ADMIN.value:
            return True

        return False
