from django.urls import path
from musicians.views import (
    AcceptInvitationView,
    AlbumDetailView,
    InvitationDetailsView,
    InvitationsListView,
    InviteCreateManyAPIView,
    MusicProjectDetailsView,
    MusicProjectGetDashboardMetricsView,
    MusicProjectImageDeleteView,
    MusicProjectInstrumentInstrumentSetDetailView,
    MusicProjectInstrumentSetAddView,
    MusicProjectInstrumentSetDeleteView,
    MusicProjectInstrumentSetView,
    MusicProjectInstrumentDetailView,
    MusicProjectInstrumentView,
    MusicProjectMemberDetailview,
    MusicProjectMembersListView,
    InvitationsPendingListView,
    MusicProjectServiceDetailView,
    MusicProjectServiceSummaryView,
    MusicProjectServiceView,
    MusicProjectTypeListCreateView,
    AlbumListView,
    MusicProjectVideoDetailView,
    MusicProjectVideoDraftDetailsView,
    MusicProjectVideoDraftView,
    MusicProjectVideoView,
    SingleDetailView,
    SingleListView,
    MusicProjectDetailsView,
    MusicProjectImageUploadView,
    MusicianProfileView,
    MusicianProjectView,
    TopicsArtistView,
    InviteCreateAPIView,
    TallyWebhookView,
    ProfileMusicProfileImageView,
    MusicProjectUpdateAboutView,
    ProfileMusicCoverImageView,
    CategoryMusicView,
    CountMusicianProfileView,
    TopcisArtistIndividualView,
    AvailabilityView,
    RecommendationMusicProjectsView
)

urlpatterns = [
    path('music-project-types/', MusicProjectTypeListCreateView.as_view(), name='music-project-type-list-create'),
    path('musician/projects/<int:pk>/albums/', AlbumListView.as_view(), name='music-project-album-list-create'),
    path('musician/projects/<int:pk>/albums/<int:album_id>/', AlbumDetailView.as_view(), name='music-project-album-details'),
    path('musician/projects/<int:pk>/singles/', SingleListView.as_view(), name='music-project-single-list-create'),
    path('musician/projects/<int:pk>/singles/<int:single_id>/', SingleDetailView.as_view(), name='music-project-single-details'),
    path('musician/projects/<int:pk>/', MusicProjectDetailsView.as_view(), name='music-project-details'),
    path('musician/projects/', MusicianProfileView.as_view(), name="musician-projects"),
    path('musician/projects/recommendations/', RecommendationMusicProjectsView.as_view(), name="recommendation-musician-projects"),
    path('musician/projects/<int:pk>/profileimage/', ProfileMusicProfileImageView.as_view(), name="update-profile-image"),
    path('musician/projects/<int:pk>/gallery/', MusicProjectImageUploadView.as_view(), name='music-project-gallery-upload'),
    path('musician/projects/<int:pk>/gallery/<int:image_id>/', MusicProjectImageDeleteView.as_view(), name='music-project-gallery-delete'),
    path('musician/projects/<int:pk>/coverimage/', ProfileMusicCoverImageView.as_view(), name="update-cover-image"),
    path('music-project/', MusicianProjectView.as_view(), name="music-project-manage"),
    path('topicsartist/', TopicsArtistView.as_view(), name="topicartis"),
    path('topicsartist/individual/', TopcisArtistIndividualView.as_view(), name="topicartist-individual"),
    path('musician/projects/<int:pk>/invitations/', InviteCreateAPIView.as_view(), name='invite-create'),
    path('musician/projects/<int:pk>/invitations-many/', InviteCreateManyAPIView.as_view(), name='invite-create'),
    path('musician/projects/<int:pk>/invitations/list/', InvitationsListView.as_view(), name='invitation-list'),
    path('musician/projects/<int:pk>/invitations/<int:invitation_id>/', InvitationDetailsView.as_view(), name='invitation-details'),
    # view pending invitations sent by a music project
    path('musician/projects/<int:pk>/invitations/pending/', InvitationsPendingListView.as_view(), name="music-project-invitations"),

    path('invitations/<int:invitation_id>/accept/<token>/', AcceptInvitationView.as_view(), name='accept-invitation'),
    path('musician/tally/verify/', TallyWebhookView.as_view(), name='tally-verify'),
    path('musician/projects/<int:pk>/about/', MusicProjectUpdateAboutView.as_view(), name="update-about-description"),
    path('musician/projects/<int:pk>/instruments/', MusicProjectInstrumentView.as_view(), name="music-project-register-new-instrument"),
    path('musician/projects/<int:pk>/instruments/<int:inventory_id>/', MusicProjectInstrumentDetailView.as_view(), name="music-project-update-instrument-inventory"),
    path('musician/projects/<int:pk>/instrument-sets/', MusicProjectInstrumentSetView.as_view(), name="music-project-instrument-sets"),
    path('musician/projects/<int:pk>/instrument-sets/<int:instrument_set_id>/', MusicProjectInstrumentSetDeleteView.as_view(), name="music-project-instrument-set-delete"),
    path('musician/projects/<int:pk>/instrument-sets/<int:instrument_set_id>/add-instrument/', MusicProjectInstrumentSetAddView.as_view(), name="music-project-instrument-sets"),
    path('musician/projects/<int:pk>/instrument-sets/<int:instrument_set_id>/instruments/<int:music_instrument_id>/', MusicProjectInstrumentInstrumentSetDetailView.as_view(), name="muisc-project-instrument-sets-instrument-detail"),
    path('musician/projects/<int:pk>/members/', MusicProjectMembersListView.as_view(), name="music-project-members"),
    path('musician/projects/<int:pk>/members/<int:member_id>/', MusicProjectMemberDetailview.as_view(), name="music-project-member-detail"),

    path('category/music/', CategoryMusicView.as_view(), name="category-music"),
    path('musicians/count', CountMusicianProfileView.as_view(), name="count-musician"),

    # musician services
    path('musician/projects/<int:pk>/services/', MusicProjectServiceView.as_view(), name="music-project-services"),
    path('musician/projects/<int:pk>/services/<int:service_id>/', MusicProjectServiceDetailView.as_view(), name="music-project-service-detail"),
    path('musician/projects/<int:pk>/services/summary/', MusicProjectServiceSummaryView.as_view(), name="music-project-service-summary"),

    # musician availability
    path('musician/projects/<int:pk>/availability/', AvailabilityView.as_view(), name="music-project-availability"),

    # music videos and drafts
    path('musician/projects/<int:pk>/videos/', MusicProjectVideoView.as_view(), name="music-project-videos"),
    path('musician/projects/<int:pk>/videos/<int:video_pk>/', MusicProjectVideoDetailView.as_view(), name="music-project-videos"),

    path('musician/projects/<int:pk>/drafts/', MusicProjectVideoDraftView.as_view(), name="music-project-videos"),
    path('musician/projects/<int:pk>/drafts/<int:draft_pk>/', MusicProjectVideoDraftDetailsView.as_view(), name="music-project-video-detail"),

    # dashboard metrics
    path('musician/projects/<int:pk>/dashboard-metrics/', MusicProjectGetDashboardMetricsView.as_view(), name="music-project-dashboard-metrics"),
]

