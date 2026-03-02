from django.urls import path
from services.views import (
    TagListCreateView,
    TagDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    ItemListCreateView,
    ItemDetailView,
    SpecificServiceListCreateView,
    SpecificServiceDetailView,
    ServiceModeListCreateView,
    ServiceModeDetailView,
    AttributeListCreateView,
    AttributeDetailView
)

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    path('specific-services/', SpecificServiceListCreateView.as_view(), name='specific-service-list-create'),
    path('specific-services/<int:pk>/', SpecificServiceDetailView.as_view(), name='specific-service-detail'),

    path('service-modes/', ServiceModeListCreateView.as_view(), name='service-mode-list-create'),
    path('service-modes/<int:pk>/', ServiceModeDetailView.as_view(), name='service-mode-detail'),

    path('attributes/', AttributeListCreateView.as_view(), name='attributes-list-create'),
    path('attributes/<int:pk>/', AttributeDetailView.as_view(), name='attributes-detail'),
]
