from django.urls import path
from core.api.views.identity_permissions import IdentityPermissionsView

urlpatterns = [
    path(
        "identity/permissions/<int:profile_id>/",
        IdentityPermissionsView.as_view(),
        name="identity-permissions"
    ),
]