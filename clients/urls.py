from django.urls import path
from clients.views import ClientTypeListView, ClientDetailListView, ClientOnboardingDifficultyListView


urlpatterns = [
    path('clients/types/', ClientTypeListView.as_view(), name='client-type-list'),
    path('clients/details/', ClientDetailListView.as_view(), name='client-details-list'),
    path('clients/difficulties/', ClientOnboardingDifficultyListView.as_view(), name='client-difficulties-list'),
]
