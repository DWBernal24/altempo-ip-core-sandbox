from datetime import datetime

from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Notification
from dashboard.permissions import IsAdministrator
from dashboard.serializers import AdminTokenObtainPairSerializer
from dashboard.serializers import LeanMusicProjectSerializer
from dashboard.serializers import ReviewMusicProjectVideoDraftSerializer
from musicians.models import Discography
from musicians.models import InstrumentSet
from musicians.models import MusicProject
from musicians.models import MusicProjectInstrument
from musicians.models import MusicProjectService
from musicians.models import MusicProjectVideoDraft
from musicians.models import MusicProjectVideoDraftStatus
from musicians.models import Single
from musicians.permissions import IsMusicProjectOwnerOrReadOnly
from musicians.serializers import DiscographySerializer
from musicians.serializers import InstrumentSetSerializer
from musicians.serializers import MusicProjectInstrumentsSerializer
from musicians.serializers import MusicProjectSerializer
from musicians.serializers import MusicProjectServiceSerializer
from musicians.serializers import SingleSerializer


class AdminLoginView(TokenObtainPairView):
    """
    Admin Login View - Only accessible to Administrators
    """

    serializer_class = AdminTokenObtainPairSerializer


class AdminListAllMusicProjectsView(generics.ListAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = LeanMusicProjectSerializer
    pagination_class = PageNumberPagination  # Offset pagination for Retool integration
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = (
            MusicProject.objects.select_related("owner")
            .prefetch_related("service_categories")
            .all()
        )

        completion_status = self.request.query_params.get("completion", None)

        if completion_status == "completed":
            queryset = queryset.filter(
                Q(isProfileInfoCompleted=True)
                & Q(isVerificationStepsCompleted=True)
                & Q(isAvailabilityCompleted=True)
            )
        elif completion_status == "pending":
            queryset = queryset.filter(
                Q(isProfileInfoCompleted=False)
                | Q(isVerificationStepsCompleted=False)
                | Q(isAvailabilityCompleted=False)
            )

        return queryset


class AdminMusicProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MusicProject.objects.all()
    serializer_class = MusicProjectSerializer
    permission_classes = [IsAdministrator]

    def get_queryset(self):
        return (
            MusicProject.objects.select_related("owner", "project_type", "owner")
            .prefetch_related(
                "service_categories",
                "musicprojectinstrument_set",
                "music_genre_tags",
                "languages",
                "topics",
                "gallery",
            )
            .all()
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        language_ids = request.data.get("languages")
        music_genre_tags_ids = request.data.get("music_genre_tags")
        if language_ids:
            instance.languages.clear()
            instance.languages.add(*language_ids)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        if music_genre_tags_ids:
            instance.music_genre_tags.clear()
            instance.music_genre_tags.add(*music_genre_tags_ids)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = datetime.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminMusicProjectBlockView(generics.GenericAPIView):
    queryset = MusicProject.objects.all()
    serializer_class = MusicProjectSerializer
    permission_classes = [IsAdministrator]

    def post(self, request, pk=None):
        """Block a music project"""
        instance = self.get_object()
        instance.is_blocked = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminMusicProjectUnblockView(generics.GenericAPIView):
    queryset = MusicProject.objects.all()
    serializer_class = MusicProjectSerializer
    permission_classes = [IsAdministrator]

    def post(self, request, pk=None):
        """Unblock a music project"""
        instance = self.get_object()
        instance.is_blocked = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminAlbumListView(generics.ListCreateAPIView):
    permission_classes = [IsAdministrator]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = DiscographySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Discography.objects.filter(music_project_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        try:
            music_project = MusicProject.objects.get(id=self.kwargs["pk"])
        except MusicProject.DoesNotExist:
            raise Http404
        serializer.save(music_project=music_project)


class ReviewMusicProjectVideoDraftView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = ReviewMusicProjectVideoDraftSerializer

    def get_queryset(self):
        return MusicProjectVideoDraft.objects.select_related("music_project")

    def get_object(self):
        queryset = self.get_queryset().filter(music_project_id=self.kwargs["pk"])

        draft = get_object_or_404(
            queryset,
            pk=self.kwargs["draft_pk"],
        )

        self.check_object_permissions(self.request, draft)

        return draft

    def partial_update(self, request, *args, **kwargs):
        # notify the users that their video has been approved/rejected

        if not self.get_object():
            raise Http404("Video not found")

        draft = self.get_object()
        music_project_owner = self.get_object().music_project.owner

        draft.review(
            status=request.data.get("status"),
            feedback=request.data.get("feedback"),
            reviewed_by=request.user,
        )

        if request.data.get("status") == MusicProjectVideoDraftStatus.ACCEPTED:
            Notification.objects.create(
                title="",  # Title will be translated in frontend
                type=Notification.VIDEO_APPROVED,
                user=music_project_owner,
                message="",  # Message will be translated in frontend
                redirect_link=f"/videos/drafts/{draft.id}",
                values={
                    "reviewer_name": request.user.name,
                    "video_id": str(draft.id),
                },
                detail="",
            )
            return Response("Video has been approved", status=status.HTTP_200_OK)

        if request.data.get("status") == MusicProjectVideoDraftStatus.REJECTED:
            Notification.objects.create(
                title="",  # Title will be translated in frontend
                type=Notification.VIDEO_REJECTED,
                user=music_project_owner,
                message="",  # Message will be translated in frontend
                redirect_link=f"/videos/drafts/{draft.id}",
                values={
                    "reviewer_name": request.user.name,
                    "video_id": str(draft.id),
                    "feedback": request.data.get("feedback", ""),
                },
                detail=request.data.get("feedback", ""),
            )
            return Response("Video has been rejected", status=status.HTTP_200_OK)

        return super().partial_update(request, *args, **kwargs)


class AdminVideoDraftListView(generics.ListAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = ReviewMusicProjectVideoDraftSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # apply filters based on the status
        status = self.request.query_params.get("status", None)

        if status == MusicProjectVideoDraftStatus.INPROCESS:
            return MusicProjectVideoDraft.objects.filter(status=status)

        if status == MusicProjectVideoDraftStatus.ACCEPTED:
            return MusicProjectVideoDraft.objects.filter(status=status)

        if status == MusicProjectVideoDraftStatus.REJECTED:
            return MusicProjectVideoDraft.objects.filter(status=status)

        return MusicProjectVideoDraft.objects.all()


class AdminMusicProjectVideoDraftListView(views.APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, pk):
        try:
            drafts = MusicProjectVideoDraft.objects.filter(music_project_id=pk)
        except MusicProjectVideoDraft.DoesNotExist:
            raise Http404

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = "page_size"
        paginator.max_page_size = 100

        paginated_queryset = paginator.paginate_queryset(drafts, request, view=self)

        if paginated_queryset is None:
            raise Http404

        serializer = ReviewMusicProjectVideoDraftSerializer(drafts, many=True)
        return paginator.get_paginated_response(serializer.data)


class AdminMusicProjectInstrumentsListView(views.APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, pk):
        try:
            instruments = MusicProjectInstrument.objects.filter(music_project_id=pk)
        except MusicProjectInstrument.DoesNotExist:
            raise Http404

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = "page_size"
        paginator.max_page_size = 100

        paginated_queryset = paginator.paginate_queryset(
            instruments, request, view=self
        )

        if paginated_queryset is None:
            raise Http404

        serializer = MusicProjectInstrumentsSerializer(instruments, many=True)
        return paginator.get_paginated_response(serializer.data)


class AdminMusicProjectInstrumentSetListView(views.APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, pk):
        try:
            instrument_sets = (
                InstrumentSet.objects.prefetch_related("instruments_in_current_set")
                .filter(music_project_id=pk)
                .all()
            )
        except InstrumentSet.DoesNotExist:
            raise Http404

        serializer = InstrumentSetSerializer(instrument_sets, many=True)
        return Response(serializer.data)


class AdminMusicProjectServicesView(views.APIView):
    permission_classes = [IsAdministrator]

    def get(self, request, pk):
        try:
            services = MusicProjectService.objects.filter(music_project_id=pk)
        except MusicProjectService.DoesNotExist:
            raise Http404

        serializer = MusicProjectServiceSerializer(services, many=True)
        return Response(serializer.data)


class AdminMusicProjectSongsView(views.APIView):
    permission_classes = [IsAdministrator]

    # endpoint for retrieving all of the Singles
    def get(self, request, pk):
        try:
            songs = Single.objects.filter(music_project_id=pk)
        except Single.DoesNotExist:
            raise Http404

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = "page_size"
        paginator.max_page_size = 100

        paginated_queryset = paginator.paginate_queryset(songs, request, view=self)

        if paginated_queryset is None:
            raise Http404

        serializer = SingleSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class AdminMusicProjectAlbumsView(views.APIView):
    permission_classes = [IsAdministrator]

    # endpoint for retrieving all of the EPs and Albums
    def get(self, request, pk):
        try:
            albums = Discography.objects.filter(music_project_id=pk)
        except Discography.DoesNotExist:
            raise Http404

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = "page_size"
        paginator.max_page_size = 100

        paginated_queryset = paginator.paginate_queryset(albums, request, view=self)

        if paginated_queryset is None:
            raise Http404

        serializer = DiscographySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
