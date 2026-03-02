from rest_framework import permissions


class IsMusicProjectOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        # Access the current music project via request
        # and check if the user is owner/member of such project
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(view, 'kwargs') and 'pk' in view.kwargs:
            pk = view.kwargs['pk']
            project = request.user.projects.filter(id=pk).first()
            if project is not None and project.owner == request.user:
                return True

        return False
