from django.urls import path
from core.views import (
    CountryListView,
    ReferralSourceListView,
    GenderListView,
    MusicalGenreTagListView,
    MusicianVoiceTypeListView,
    TimeZoneView,
    VocalStyleListView,
    InstrumentListView,
    DJTypeListView,
    CollabTypeListView,
    EquipmentListView,
    LanguagesListView,
    NotificationView
)

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('timezones/', TimeZoneView.as_view(), name='timezone-list'),
    path('referral-sources/', ReferralSourceListView.as_view(), name='referral-source-list'),
    path('genders/', GenderListView.as_view(), name='gender-list'),
    path('musical-genres/', MusicalGenreTagListView.as_view(), name='musical-genres-list'),
    path('musician-voices-types/', MusicianVoiceTypeListView.as_view(), name='musician-voice-types-list'),
    path('vocal-styles/', VocalStyleListView.as_view(), name='vocal-styles-list'),
    path('instruments/', InstrumentListView.as_view(), name='instruments-list'),
    path('dj-types/', DJTypeListView.as_view(), name='dj-types-list'),
    path('collab-types/', CollabTypeListView.as_view(), name='collab-types-list'),
    path('equipment/', EquipmentListView.as_view(), name='equipment-list'),
    path('languages/', LanguagesListView.as_view(), name='laguages-list'),
    path('notifications/', NotificationView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationView.as_view(), name='notifications-mark-read')
]
