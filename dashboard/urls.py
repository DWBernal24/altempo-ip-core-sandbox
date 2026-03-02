from dj_rest_auth.views import LoginView
from django.urls import path

from dashboard.views import (
    AdminAlbumListView,
    AdminListAllMusicProjectsView,
    AdminLoginView,
    AdminMusicProjectAlbumsView,
    AdminMusicProjectDetailsView,
    AdminMusicProjectBlockView,
    AdminMusicProjectUnblockView,
    AdminMusicProjectInstrumentSetListView,
    AdminMusicProjectInstrumentsListView,
    AdminMusicProjectServicesView,
    AdminMusicProjectSongsView,
    AdminVideoDraftListView,
    ReviewMusicProjectVideoDraftView,
    AdminMusicProjectVideoDraftListView,
)


urlpatterns = [
    # Administrator Login
    path(
        "login/",
        AdminLoginView.as_view(),
        name="admin_login",
    ),
    path(
        "music-projects/",
        AdminListAllMusicProjectsView.as_view(),
        name="music-projects",
    ),
    path(
        "music-projects/<int:pk>/",
        AdminMusicProjectDetailsView.as_view(),
        name="music-projects",
    ),
    path(
        "music-projects/<int:pk>/block/",
        AdminMusicProjectBlockView.as_view(),
        name="admin-music-project-block",
    ),
    path(
        "music-projects/<int:pk>/unblock/",
        AdminMusicProjectUnblockView.as_view(),
        name="admin-music-project-unblock",
    ),
    path(
        "music-projects/<int:pk>/albums/",
        AdminAlbumListView.as_view(),
        name="music-project-albums-list",
    ),
    path(
        "music-projects/<int:pk>/instruments/",
        AdminMusicProjectInstrumentsListView.as_view(),
        name="music-project-instruments-list",
    ),
    path(
        "music-projects/<int:pk>/instrument-sets/",
        AdminMusicProjectInstrumentSetListView.as_view(),
        name="music-project-instruments-set-list",
    ),
    path(
        "music-projects/<int:pk>/services/",
        AdminMusicProjectServicesView.as_view(),
        name="music-project-services-list",
    ),
    # Discography and Music for endpoints
    path(
        "music-projects/<int:pk>/singles/",
        AdminMusicProjectSongsView.as_view(),
        name="music-project-singles",
    ),
    path(
        "music-projects/<int:pk>/albums/",
        AdminMusicProjectAlbumsView.as_view(),
        name="music-project-albums",
    ),
    # video draft list and reviews
    path(
        "music-projects/<int:pk>/videos/<int:draft_pk>/review/",
        ReviewMusicProjectVideoDraftView.as_view(),
        name="music-project-videos",
    ),
    path(
        "music-projects/<int:pk>/videos/",
        AdminMusicProjectVideoDraftListView.as_view(),
        name="music-project-video-drafts",
    ),
    path(
        "drafts/pending/",
        AdminVideoDraftListView.as_view(),
        name="music-project-video-drafts",
    ),
]
