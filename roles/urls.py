from django.urls import path
from roles.views import (
    RoleListCreateView, UserProfileCreateView, UserProfileGetView,
    DemografyView, KeyDatesView, ListDeListDemografyProfileView,
    KeyDatesProfileView
)

urlpatterns = [
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('users/profile', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('me/profile/', UserProfileGetView.as_view(), name='get-user-profile'),
    path('demografy/', DemografyView.as_view(), name="demografy-base"),
    path('keydates/', KeyDatesView.as_view(), name="keydates-base"),
    path('list-demografy-profile/', ListDeListDemografyProfileView.as_view(), name="demografy-profile"),
    path('list-keydates-profile/', KeyDatesProfileView.as_view(), name="keydates-profile")
]
