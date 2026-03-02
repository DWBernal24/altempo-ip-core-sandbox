import base64
import hashlib
import hmac

from allauth.account.views import PermissionDenied
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.db.models import F
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.generic.base import logger
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import serializers
from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Notification
from musicians.models import AvailabilityInfo
from musicians.models import CategoryMusic
from musicians.models import Discography
from musicians.models import InstrumentSet
from musicians.models import InviteMemberBand
from musicians.models import MusicProject
from musicians.models import MusicProjectImage
from musicians.models import MusicProjectInstrument
from musicians.models import MusicProjectInstrumentInstrumentSet
from musicians.models import MusicProjectService
from musicians.models import MusicProjectType
from musicians.models import MusicProjectVideo
from musicians.models import MusicProjectVideoDraft
from musicians.models import MusicProjectVideoDraftStatus
from musicians.models import Single
from musicians.models import TopicArtist
from musicians.models import User
from musicians.permissions import IsMusicProjectOwnerOrReadOnly
from musicians.serializers import AvailabilityInfoSerializer, InstrumentInSetQuantitySerializer, InstrumentInSetSerializer, InviteMemberLeanSerializer
from musicians.serializers import AvailabilityInfoUpdateSerializer
from musicians.serializers import BasicCreateMusicProjectSerializer
from musicians.serializers import CategoryMusicSerializer
from musicians.serializers import DiscographySerializer
from musicians.serializers import InstrumentSetSerializer
from musicians.serializers import InviteMemberBandCreateManySerializer
from musicians.serializers import InviteMemberBandCreateSerializer
from musicians.serializers import InviteMemberBandSerializer
from musicians.serializers import MusicProjectImageSerializer
from musicians.serializers import MusicProjectInstrumentsSerializer
from musicians.serializers import MusicProjectMemberSerializer
from musicians.serializers import MusicProjectSerializer
from musicians.serializers import MusicProjectServiceCreateSerializer
from musicians.serializers import MusicProjectServiceSerializer
from musicians.serializers import MusicProjectServiceSummarySerializer
from musicians.serializers import MusicProjectTypeSerializer
from musicians.serializers import MusicProjectUpdateAboutSerializer
from musicians.serializers import MusicProjectVideoDraftCreateSerializer
from musicians.serializers import MusicProjectVideoDraftSerializer
from musicians.serializers import MusicProjectVideoSerializer
from musicians.serializers import ProfileMusicianCoverImageSerializer
from musicians.serializers import ProfileMusicianProfileImageSerializer
from musicians.serializers import SingleSerializer
from musicians.serializers import TopicArtistSerializer
from services.models import Category
from utils.band_invite import send_invitation_email
from utils.displaySchedule import get_musician_schedule_in_timezone
from utils.email import send_email_basic


class CategoryMusicView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = CategoryMusic
    serializer_class = CategoryMusicSerializer

    def get(self, request):
        genre_ids = request.query_params.getlist("genre_musics")
        service_ids = request.query_params.getlist("orderservices")
        language_ids = request.query_params.getlist("language_ids")
        topic_ids = request.query_params.getlist("topic_ids")

        paginator = PageNumberPagination()

        instances = self.model.objects.all()

        # Aplicar filtros si existen
        if genre_ids:
            instances = instances.filter(music_genre_tags__in=genre_ids)
        if service_ids:
            instances = instances.filter(orderservices__in=service_ids)
        if language_ids:
            instances = instances.filter(languages__in=language_ids)
        if topic_ids:
            instances = instances.filter(topics__in=topic_ids)

        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProfileMusicCoverImageView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, pk):
        try:
            music_project = MusicProject.objects.get(id=pk)
        except MusicProject.DoesNotExist:
            return response.Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializers = ProfileMusicianCoverImageSerializer(
            music_project, data=request.data, partial=True
        )
        if serializers.is_valid():
            serializers.save()
            return response.Response(
                {
                    "message": "Imagen actualizada correctamente",
                    "data": serializers.data,
                }
            )
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicProjectUpdateAboutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            music_project = MusicProject.objects.get(id=pk)
        except MusicProject.DoesNotExist:
            return response.Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializers = MusicProjectUpdateAboutSerializer(
            music_project, data=request.data, partial=True
        )
        if serializers.is_valid():
            serializers.save()
            return response.Response(
                {
                    "message": "Imagen actualizada correctamente",
                    "data": serializers.data,
                }
            )
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileMusicProfileImageView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, pk):
        try:
            music_project = MusicProject.objects.get(id=pk)
        except MusicProject.DoesNotExist:
            return response.Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializers = ProfileMusicianProfileImageSerializer(
            music_project, data=request.data, partial=True
        )
        if serializers.is_valid():
            serializers.save()
            return response.Response(
                {
                    "message": "Imagen actualizada correctamente",
                    "data": serializers.data,
                }
            )
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicsArtistView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = TopicArtist
    serializer_class = TopicArtistSerializer

    def get(self, request):
        paginator = PageNumberPagination()
        instances = self.model.objects.all()
        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TopcisArtistIndividualView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        topic_individual = TopicArtist.objects.get(individual=True)
        serializar = TopicArtistSerializer(topic_individual)
        return response.Response(serializar.data)


class MusicianProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = MusicProject
    serializer_class = MusicProjectSerializer

    def get(self, request):

        genre_ids = request.query_params.getlist("genre_musics")
        service_ids = request.query_params.getlist("orderservices")
        language_ids = request.query_params.getlist("language_ids")
        topic_ids = request.query_params.getlist("topic_ids")
        categories = request.query_params.getlist("categories")

        paginator = PageNumberPagination()

        instances = self.model.objects.all()
        instances = instances.select_related('owner', 'project_type') \
            .prefetch_related('music_genre_tags', 'orderservices', 'languages', 'topics', 'categories', 'service_categories', 'members', 'gallery')

        if genre_ids:
            instances = instances.filter(music_genre_tags__in=genre_ids)
        if service_ids:
            instances = instances.filter(order_services__in=service_ids)
        if language_ids:
            instances = instances.filter(languages__in=language_ids)
        if topic_ids:
            instances = instances.filter(topics__in=topic_ids)
        if categories:
            instances = instances.filter(categories__in=categories)

        instances = instances.distinct()

        result_page = paginator.paginate_queryset(instances, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CountMusicianProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    model = MusicProject
    serializer_class = MusicProjectSerializer

    def get(self, request):
        genre_ids = request.query_params.get("genre_musics")
        service_ids = request.query_params.get("orderservices")
        language_ids = request.query_params.get("language_ids")
        topic_ids = request.query_params.get("topic_ids")
        categories = request.query_params.get("categories")

        instances = self.model.objects.all()

        # Aplicar filtros si existen
        if genre_ids:
            instances = instances.filter(music_genre_tags__in=genre_ids)
        if service_ids:
            instances = instances.filter(order_services__in=service_ids)
        if language_ids:
            instances = instances.filter(languages__in=language_ids)
        if topic_ids:
            instances = instances.filter(topics__in=topic_ids)
        if categories:
            instances = instances.filter(categories__in=categories)
        count = instances.count()
        return response.Response({"musicians": count}, status=status.HTTP_200_OK)


class MusicProjectTypeListCreateView(views.APIView):
    @extend_schema(
        summary="Get a list of music project types",
        description="Get a list of music project types",
        responses={200: MusicProjectTypeSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        music_project_types = MusicProjectType.objects.all()
        result_page = paginator.paginate_queryset(music_project_types, request)
        serializer = MusicProjectTypeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MusicianProjectView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.copy()

        serializer = BasicCreateMusicProjectSerializer(data=data)
        if serializer.is_valid():
            try:
                project_type = MusicProjectType.objects.get(
                    id=serializer.validated_data.get("music_project_type_id")
                )
            except MusicProjectType.DoesNotExist:
                return response.Response(
                    {"error": "Tipo de proyecto no válido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            music_project = MusicProject.objects.create(
                name=serializer.validated_data.get("music_project_name", user.name),
                owner=user,
                project_type=project_type,
                birth_date=user.profile.birth_date,
                phone_number=user.profile.phone_number,
                country=user.profile.country,
            )

            # create new availability entry for each musician
            AvailabilityInfo.objects.create(music_project=music_project)

            for service_type_id in serializer.validated_data.get("services"):
                service = Category.objects.get(id=service_type_id)
                music_project.service_categories.add(service)

            serializer_music_project = MusicProjectSerializer(
                music_project
            )  # ← Aquí está el cambio importante
            return response.Response(
                serializer_music_project.data, status=status.HTTP_201_CREATED
            )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        music_project = MusicProject.objects.get(owner=user)
        if not music_project:
            return response.Response(
                {"detail": "No music project found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MusicProjectImageSerializer(data=music_project)
        return serializer.data


class SingleListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]
    serializer_class = SingleSerializer

    def get_queryset(self):
        return Single.objects.filter(
            music_project_id=self.kwargs["pk"],
        )

    def perform_create(self, serializer):
        try:
            music_project = MusicProject.objects.get(id=self.kwargs["pk"])
        except MusicProject.DoesNotExist:
            raise Http404
        # check if the user has less than 6 songs; otherwise, return an error
        if music_project.singles.count() >= 6:
            raise ValidationError("Limite de canciones alcanzado")
        serializer.save(music_project=music_project)


class SingleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]
    serializer_class = SingleSerializer

    def get_object(self):
        return Single.objects.get(
            id=self.kwargs["single_id"], music_project_id=self.kwargs["pk"]
        )


class AlbumListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = DiscographySerializer

    def get_queryset(self):
        return Discography.objects.filter(music_project_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        try:
            music_project = MusicProject.objects.get(id=self.kwargs["pk"])
        except MusicProject.DoesNotExist:
            raise Http404

        # check if user has less than 6 albums created; otherwise, return an error
        discography = music_project.discography
        albums = discography.filter(type=Discography.TYPE_CHOICES[0][0]).count()
        eps = discography.filter(type=Discography.TYPE_CHOICES[1][0]).count()

        if albums >= 6 or eps >= 6:
            raise ValidationError("Limite de albums alcanzado")
        serializer.save(music_project=music_project)


class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscographySerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get_object(self):
        return Discography.objects.get(
            id=self.kwargs["album_id"],
            music_project_id=self.kwargs["pk"],
        )


class MusicProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MusicProject.objects.all()
    serializer_class = MusicProjectSerializer
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

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


class MusicProjectImageUploadView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            project = MusicProject.objects.get(id=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Music project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # max images: 8
        if project.gallery.count() >= 8:
            return Response(
                {"detail": "Limite de imagenes alcanzado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["music_project_id"] = project.id
        serializer = MusicProjectImageSerializer(data=data)

        if serializer.is_valid():
            serializer.save(music_project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicProjectImageDeleteView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def delete(self, request, pk, image_id):
        """
        Delete an image uploaded by the user, from both the main database and S3.
        """
        try:
            project = MusicProject.objects.get(id=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Music project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            image = MusicProjectImage.objects.get(id=image_id, music_project=project)
        except MusicProjectImage.DoesNotExist:
            return Response(
                {"detail": "Image not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if image.image:
            image.image.delete(save=False)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class InviteCreateAPIView(generics.CreateAPIView):
    serializer_class = InviteMemberBandCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["music_project"] = get_object_or_404(MusicProject, id=self.kwargs["pk"])
        context["request"] = self.request

        return context

    def create(self, request, *args, **kwargs):
        from django.utils.translation import gettext as _

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        music_project = get_object_or_404(MusicProject, id=self.kwargs["pk"])
        if music_project.owner != self.request.user:
            raise PermissionDenied(_("You are not the owner of this project."))

        if music_project.project_type.name == "INDIVIDUAL":
            return Response(
                {"detail": _("You can't invite members to an individual project.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation = serializer.save()

        try:
            send_invitation_email(invitation, self.request)
            # Create the notification for the recipient user, if the user is already registered
            if invitation.invited_user:
                Notification.objects.create(
                    title="",  # Title will be translated in frontend
                    type=Notification.INVITE_BAND_MEMBER,
                    user=invitation.invited_user,
                    message="",  # Message will be translated in frontend
                    redirect_link=f"/invitations/{invitation.id}",
                    values={
                        "band_name": invitation.music_project.name,
                        "owner_name": invitation.music_project.owner.name,
                        "invitation_id": str(invitation.id),
                    },
                    detail=invitation.message or "",
                )

            return Response(
                {
                    "message": _("Invitation sent successfully."),
                    "invitation_id": invitation.id,
                    "email": invitation.email,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            invitation.delete()
            return Response(
                {
                    "error": _(
                        "Failed to send invitation email. Please try again later."
                    ),
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InviteCreateManyAPIView(generics.CreateAPIView):
    serializer_class = InviteMemberBandCreateManySerializer
    permission_classes = [permissions.IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["music_project"] = get_object_or_404(MusicProject, id=self.kwargs["pk"])
        context["request"] = self.request

        return context

    def create(self, request, *args, **kwargs):
        from django.utils.translation import gettext as _

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        music_project = get_object_or_404(MusicProject, id=self.kwargs["pk"])
        if music_project.owner != self.request.user:
            raise PermissionDenied(_("You are not the owner of this project."))

        if music_project.project_type.name == "INDIVIDUAL":
            return Response(
                {"detail": _("You can't invite members to an individual project.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_invitations = serializer.save()

        for invitation in created_invitations:
            try:
                invitation_token = invitation.generate_token()
                send_invitation_email(invitation, invitation_token, self.request)
                # Create the notification for the recipient user, if the user is already registered
                if invitation.invited_user:
                    Notification.objects.create(
                        title="",  # Title will be translated in frontend
                        type=Notification.INVITE_BAND_MEMBER,
                        user=invitation.invited_user,
                        message="",  # Message will be translated in frontend
                        redirect_link=f"/invitations/{invitation.id}/accept/{invitation_token}",
                        values={
                            "band_name": invitation.music_project.name,
                            "owner_name": invitation.music_project.owner.name,
                            "invitation_id": str(invitation.id),
                            "invitation_token": invitation_token,
                        },
                        detail=invitation.message or "",
                    )

            except Exception as e:
                invitation.delete()
                return Response(
                    {
                        "error": _(
                            "Failed to send invitation email. Please try again later."
                        ),
                        "detail": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "message": _("Invitations sent successfully."),
                "invitations": [invitation.id for invitation in created_invitations],
                "emails": [invitation.email for invitation in created_invitations],
            },
            status=status.HTTP_201_CREATED,
        )


class AcceptInvitationView(views.APIView):
    def get(self, request, invitation_id, token):
        """
        Handle via Email link
        For this, the URL has an invitation token that we must parse
        to get the information of the user that received the email
        (assuming that the user already has an account, of course)
        Returns HTML template for browser viewing
        """
        # Activate user's preferred language
        user_language = (
            request.user.language.code
            if hasattr(request.user, "language") and request.user.language
            else "en_US"
        )
        current_language = get_language()
        activate(user_language)

        try:
            invitation = get_object_or_404(InviteMemberBand, id=invitation_id)

            # Common context for all templates
            context = {
                "user_name": invitation.email,
                "band_name": invitation.music_project.name,
                "dashboard_url": f"{settings.FRONTEND_URL}/dashboard"
                if hasattr(settings, "FRONTEND_URL")
                else "/dashboard",
                "help_center_url": f"{settings.FRONTEND_URL}/help"
                if hasattr(settings, "FRONTEND_URL")
                else "/help",
                "terms_url": f"{settings.FRONTEND_URL}/terms"
                if hasattr(settings, "FRONTEND_URL")
                else "/terms",
                "privacy_url": f"{settings.FRONTEND_URL}/privacy"
                if hasattr(settings, "FRONTEND_URL")
                else "/privacy",
                "unsubscribe_url": f"{settings.FRONTEND_URL}/unsubscribe"
                if hasattr(settings, "FRONTEND_URL")
                else "/unsubscribe",
                "instagram_url": "https://instagram.com/altempo",
                "linkedin_url": "https://linkedin.com/altempo",
                "facebook_url": "https://facebook.com/altempo",
            }

            if invitation.is_expired:
                invitation.expire()
                context["error_message"] = _("The invitation has expired.")
                return TemplateResponse(
                    request, "emails/invitation_error.html", context
                )

            if invitation.status != InviteMemberBand.STATUS_CHOICES[2][0]:
                context["error_message"] = _(
                    "The invitation has already been accepted or declined."
                )
                return TemplateResponse(
                    request, "emails/invitation_error.html", context
                )

            action = request.query_params.get("action")
            if action != "accept" and action != "decline":
                context["error_message"] = _(
                    "Invalid action. Please use the link from your invitation email."
                )
                return TemplateResponse(
                    request, "emails/invitation_error.html", context
                )

            if not token:
                context["error_message"] = _(
                    "Missing authentication token. Please use the link from your invitation email."
                )
                return TemplateResponse(
                    request, "emails/invitation_error.html", context
                )

            verified_invitation, error = InviteMemberBand.verify_token(token)

            if error:
                context["error_message"] = _(error)
                return TemplateResponse(
                    request, "emails/invitation_error.html", context
                )

            # Process the action
            if action == "accept":
                try:
                    verified_invitation.accept(email=invitation.email)

                    # Send notification to band owner
                    Notification.objects.create(
                        title="",  # Title will be translated in frontend
                        type=Notification.INVITE_BAND_CONFIRMED,
                        user=verified_invitation.music_project.owner,
                        message="",  # Message will be translated in frontend
                        redirect_link=f"/bands/{verified_invitation.music_project.id}",
                        values={
                            "band_name": verified_invitation.music_project.name,
                            "user_name": verified_invitation.email,
                            "invitation_id": str(verified_invitation.id),
                        },
                        detail="",
                    )

                    # Add band URL to context
                    context["band_url"] = f"https://altempo.dev/music/"
                    return TemplateResponse(
                        request, "emails/invitation_accepted.html", context
                    )

                except ValueError as e:
                    context["error_message"] = str(e)
                    return TemplateResponse(
                        request, "emails/invitation_error.html", context
                    )

            elif action == "decline":
                try:
                    verified_invitation.decline()

                    # Send notification to band owner
                    Notification.objects.create(
                        title="",  # Title will be translated in frontend
                        type=Notification.INVITE_BAND_DECLINED,
                        user=verified_invitation.music_project.owner,
                        message="",  # Message will be translated in frontend
                        redirect_link=f"/bands/{verified_invitation.music_project.id}",
                        values={
                            "band_name": verified_invitation.music_project.name,
                            "user_name": request.user.name or request.user.email,
                            "invitation_id": str(verified_invitation.id),
                        },
                        detail="",
                    )

                    return TemplateResponse(
                        request, "emails/invitation_declined.html", context
                    )

                except ValueError as e:
                    context["error_message"] = str(e)
                    return TemplateResponse(
                        request, "emails/invitation_error.html", context
                    )

        except Exception as e:
            logger.error(f"Error processing invitation: {str(e)}")
            context = {
                "user_name": request.user.name or request.user.email,
                "error_message": _(
                    "An unexpected error occurred. Please try again or contact support."
                ),
                "dashboard_url": f"{settings.FRONTEND_URL}/dashboard"
                if hasattr(settings, "FRONTEND_URL")
                else "/dashboard",
                "help_center_url": f"{settings.FRONTEND_URL}/help"
                if hasattr(settings, "FRONTEND_URL")
                else "/help",
                "terms_url": f"{settings.FRONTEND_URL}/terms"
                if hasattr(settings, "FRONTEND_URL")
                else "/terms",
                "privacy_url": f"{settings.FRONTEND_URL}/privacy"
                if hasattr(settings, "FRONTEND_URL")
                else "/privacy",
                "unsubscribe_url": f"{settings.FRONTEND_URL}/unsubscribe"
                if hasattr(settings, "FRONTEND_URL")
                else "/unsubscribe",
                "instagram_url": "https://instagram.com/altempo",
                "linkedin_url": "https://linkedin.com/altempo",
                "facebook_url": "https://facebook.com/altempo",
            }
            return TemplateResponse(request, "emails/invitation_error.html", context)

        finally:
            # Restore original language
            activate(current_language)

    def patch(self, request, invitation_id):
        """
        Handle via API (PATCH)
        """

        invitation = get_object_or_404(InviteMemberBand, id=invitation_id)
        action = request.data.get("action")

        if invitation.is_expired:
            invitation.expire()
            return Response(
                {"detail": "The invitation has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "accept":
            try:
                invitation.accept(request.user)

                # send a notification to the band that sent the invitation
                Notification.objects.create(
                    title="",  # Title will be translated in frontend
                    type=Notification.INVITE_BAND_CONFIRMED,
                    user=invitation.music_project.owner,
                    message="",  # Message will be translated in frontend
                    redirect_link=f"/bands/{invitation.music_project.id}",
                    values={
                        "band_name": invitation.music_project.name,
                        "user_name": request.user.name,
                        "invitation_id": str(invitation.id),
                    },
                    detail="",
                )

                return Response(
                    {
                        "message": "Invitation accepted successfully.",
                        "music_project": MusicProjectSerializer(
                            invitation.music_project
                        ).data,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "error": "Failed to accept invitation. Please try again later.",
                        "detail": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        elif action == "decline":
            try:
                invitation.decline()

                # send a notification to the band that sent the invitation
                Notification.objects.create(
                    title="",  # Title will be translated in frontend
                    type=Notification.INVITE_BAND_DECLINED,
                    user=invitation.music_project.owner,
                    message="",  # Message will be translated in frontend
                    redirect_link=f"/bands/{invitation.music_project.id}",
                    values={
                        "band_name": invitation.music_project.name,
                        "user_name": request.user.name,
                        "invitation_id": str(invitation.id),
                    },
                    detail="",
                )

                return Response(
                    {
                        "message": "Invitation declined successfully.",
                        "music_project": MusicProjectSerializer(
                            invitation.music_project
                        ).data,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "error": "Failed to decline invitation. Please try again later.",
                        "detail": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {"message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST
        )


class InvitationsListView(generics.ListAPIView):
    serializer_class = InviteMemberBandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        music_project_id = self.kwargs["pk"]
        music_project = get_object_or_404(MusicProject, id=music_project_id)

        if music_project.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this project.")

        return InviteMemberBand.objects.filter(music_project=music_project)


class InvitationDetailsView(generics.RetrieveDestroyAPIView):
    serializer_class = InviteMemberBandSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        invitation_id = self.kwargs["invitation_id"]
        return get_object_or_404(InviteMemberBand, id=invitation_id)


class InvitationsPendingListView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        invites = InviteMemberBand.objects.filter(music_project_id=pk, status=InviteMemberBand.STATUS_INPROCESS)
        serializer = InviteMemberLeanSerializer(invites, many=True)
        return Response(serializer.data)


class TallyWebhookView(views.APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        received_sig = request.headers.get("Tally-Signature")

        # Verificar firma (si usas 'signingSecret')
        if hasattr(settings, "TALLY_SIGNING_SECRET"):
            secret = settings.TALLY_SIGNING_SECRET.encode()
            expected_sig = base64.b64encode(
                hmac.new(secret, payload, hashlib.sha256).digest()
            ).decode()

            if received_sig != expected_sig:
                return Response(
                    {"error": "Firma inválida"}, status=status.HTTP_401_UNAUTHORIZED
                )

        # Procesar los datos del formulario
        data = request.data
        print("📩 Webhook recibido:", data)

        # Aquí podrías guardar la respuesta en tu modelo, enviar un email, etc.
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class MusicProjectInstrumentPagination(PageNumberPagination):
    page_size = 10  # Set your desired default page size
    page_size_query_param = (
        "page_size"  # Optional: allow clients to override with ?page_size=X
    )
    max_page_size = 20  # Optional: set a maximum limit


class MusicProjectInstrumentView(generics.ListCreateAPIView):
    serializer_class = MusicProjectInstrumentsSerializer
    permission_classes = [IsMusicProjectOwnerOrReadOnly]
    pagination_class = (
        MusicProjectInstrumentPagination  # Use your custom pagination class
    )

    def get_queryset(self):
        queryset = MusicProjectInstrument.objects.filter(
            music_project_id=self.kwargs["pk"]
        )
        instrument_type = self.request.query_params.get("type", None)
        if instrument_type is None:
            return queryset
        return queryset.filter(instrument__type=instrument_type)

    def perform_create(self, serializer):
        try:
            music_project = MusicProject.objects.get(id=self.kwargs["pk"])
        except MusicProject.DoesNotExist:
            raise Http404
        serializer.save(music_project=music_project)


class MusicProjectInstrumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]
    queryset = MusicProjectInstrument.objects.all()
    serializer_class = MusicProjectInstrumentsSerializer

    def get_object(self):
        music_project_id = self.kwargs.get("pk")
        music_project_instrument_id = self.kwargs.get("inventory_id")

        try:
            return (
                self.get_queryset()
                .filter(
                    music_project_id=music_project_id,
                    id=music_project_instrument_id,
                )
                .first()
            )
        except MusicProjectInstrument.DoesNotExist:
            raise Http404


class MusicProjectInstrumentSetView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            project = MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        project_instruments = (
            InstrumentSet.objects.filter(music_project=project)
            .select_related("music_project")
            .prefetch_related(
                "musicprojectinstrumentinstrumentset_set__music_project_instrument"
            )
            .annotate(
                db_calculated_total_price=Sum(
                    F("musicprojectinstrumentinstrumentset__quantity_for_set")
                    * F(
                        "musicprojectinstrumentinstrumentset__music_project_instrument__price_per_instrument"
                    )
                )
            )
        )

        serializer = InstrumentSetSerializer(project_instruments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            project = MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data["music_project"] = project.id
        serializer = InstrumentSetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(music_project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicProjectInstrumentInstrumentSetDetailView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk, instrument_set_id, music_instrument_id):
        try:
            MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            instrument_in_set = MusicProjectInstrumentInstrumentSet.objects.get(pk=music_instrument_id)
        except InstrumentSet.DoesNotExist:
            return Response(
                {"detail": "Instrument in set not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InstrumentInSetSerializer(instrument_in_set)
        return Response(serializer.data)

    def patch(self, request, pk, instrument_set_id, music_instrument_id):
        try:
            MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            instrument_in_set = MusicProjectInstrumentInstrumentSet.objects.get(pk=music_instrument_id)
        except InstrumentSet.DoesNotExist:
            return Response(
                {"detail": "Instrument in set not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InstrumentInSetQuantitySerializer(instrument_in_set, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValueError:
                return Response(
                    {"detail": "Not enough instruments to add to current set"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, instrument_set_id, music_instrument_id):
        try:
            MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            instrument_in_set = MusicProjectInstrumentInstrumentSet.objects.get(pk=music_instrument_id)
        except InstrumentSet.DoesNotExist:
            return Response(
                {"detail": "Instrument in set not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instrument_in_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicProjectInstrumentSetAddView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def post(self, request, pk, instrument_set_id):
        try:
            MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        music_instrument_id = request.data.get("instrument")
        try:
            instrument_set = InstrumentSet.objects.get(pk=instrument_set_id)
        except InstrumentSet.DoesNotExist:
            return Response(
                {"detail": "Instrument set not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if music_instrument_id:
            music_instrument = MusicProjectInstrument.objects.get(
                pk=music_instrument_id
            )

            # work with the through relationship
            through, created = (
                MusicProjectInstrumentInstrumentSet.objects.get_or_create(
                    music_project_instrument=music_instrument,
                    instrument_set=instrument_set,
                    defaults={"quantity_for_set": self.request.data.get("quantity", 1)},
                )
            )

            if not created:
                through.quantity_for_set += self.request.data.get("quantity", 1)
                through.save()

        serializer = InstrumentSetSerializer(instrument_set)
        return Response(serializer.data)


class MusicProjectInstrumentSetDeleteView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def delete(self, request, pk, instrument_set_id):
        try:
            MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            instrument_set = InstrumentSet.objects.get(pk=instrument_set_id)
        except InstrumentSet.DoesNotExist:
            return Response(
                {"detail": "Instrument set not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instrument_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicProjectMembersListView(generics.ListAPIView):
    serializer_class = MusicProjectMemberSerializer
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get_queryset(self):
        # get many to many collectoin
        return MusicProject.objects.get(id=self.kwargs["pk"]).members.all()


class MusicProjectMemberDetailview(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def delete(self, request, pk, member_id):
        try:
            music_project = MusicProject.objects.get(pk=pk, owner=request.user)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Project not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            member = User.objects.get(pk=member_id)
            music_project.members.remove(member)  # Does nothing if not a member
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class MusicProjectServiceView(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        services = MusicProjectService.objects.filter(music_project_id=pk)
        serializer = MusicProjectServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = MusicProjectServiceCreateSerializer(
            data=request.data,
            context={
                "music_project_id": pk,
            },
        )
        if serializer.is_valid():
            music_project = MusicProject.objects.get(id=pk)
            service = serializer.save(music_project=music_project)

            response_serializer = MusicProjectServiceSerializer(service)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MusicProjectServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]
    queryset = MusicProjectService.objects.all()
    serializer_class = MusicProjectServiceSerializer

    def get_object(self):
        try:
            service = MusicProjectService.objects.get(
                music_project_id=self.kwargs["pk"], id=self.kwargs["service_id"]
            )
        except MusicProjectService.DoesNotExist:
            raise Http404

        return service


class MusicProjectServiceSummaryView(views.APIView):
    def get(self, request, pk):
        """
        Get the top three ACTIVE services ordered by creation date
        """
        services = MusicProjectService.objects.filter(
            music_project_id=pk, is_active=True
        ).order_by("-created_at")[:3]
        serializer = MusicProjectServiceSummarySerializer(services, many=True)
        return Response(serializer.data)


class AvailabilityListView(generics.ListAPIView):
    serializer_class = AvailabilityInfoSerializer

    def get_queryset(self):
        return AvailabilityInfo.objects.filter(music_project_id=self.kwargs["pk"])


class AvailabilityView(views.APIView):
    permission_classes = [IsAuthenticated, IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            musician = MusicProject.objects.prefetch_related("availability_info").get(
                id=pk
            )
        except AvailabilityInfo.DoesNotExist:
            return Response(
                {"detail": "Availability not found or unauthorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AvailabilityInfoSerializer(
            musician.availability_info, context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            availability = AvailabilityInfo.objects.get(music_project_id=pk)
        except AvailabilityInfo.DoesNotExist:
            # create a new availability object for the music project
            availability = AvailabilityInfo.objects.create(music_project_id=pk)
            availability.save()

        serializer = AvailabilityInfoUpdateSerializer(
            availability, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicProjectVideoView(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        videos = MusicProjectVideo.objects.filter(music_project_id=pk)
        serializer = MusicProjectVideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        For creating new music video entries, first the user has to upload
        a draft of the video they want to upload. Then, they should wait
        for their administrator to approve or reject the proposal
        """
        serializer = MusicProjectVideoDraftCreateSerializer(data=request.data)
        if serializer.is_valid():
            draft = serializer.save(music_project_id=pk)
            response_serializer = MusicProjectVideoDraftSerializer(draft)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MusicProjectVideoDetailView(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk, video_pk):
        video = MusicProjectVideo.objects.get(id=video_pk)
        serializer = MusicProjectVideoSerializer(video)
        return Response(serializer.data)

    def delete(self, request, pk, video_pk):
        video = MusicProjectVideo.objects.get(id=video_pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicProjectVideoDraftView(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk):
        videos = MusicProject.objects.get(id=pk).video_drafts

        # add filters
        status = request.query_params.get("status")

        if (
            status == MusicProjectVideoDraftStatus.INPROCESS
            or status == MusicProjectVideoDraftStatus.ACCEPTED
            or status == MusicProjectVideoDraftStatus.REJECTED
        ):
            videos = videos.filter(status=status)

        serializer = MusicProjectVideoDraftSerializer(videos, many=True)
        return Response(serializer.data)


class MusicProjectVideoDraftDetailsView(views.APIView):
    permission_classes = [IsMusicProjectOwnerOrReadOnly]

    def get(self, request, pk, draft_pk):
        draft = MusicProjectVideoDraft.objects.get(id=draft_pk)
        serializer = MusicProjectVideoDraftSerializer(draft)
        return Response(serializer.data)

    def delete(self, request, pk, draft_pk):
        draft = MusicProjectVideoDraft.objects.get(id=draft_pk)
        draft.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicProjectGetDashboardMetricsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Get the main metrics that are displayed in the home dashboard for a Music Project:
        1. Finished events (completed orders)
        2. Next Event (date of the next event)
        3. Last month's income (total of the last month in orders)
        4. Total Active Services
        """
        try:
            music_project = MusicProject.objects.get(id=pk)
        except MusicProject.DoesNotExist:
            return Response(
                {"detail": "Music Project does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        orders = music_project.orders.all()

        # 1. Finished events (completed orders)
        completed_orders = orders.filter(status="ORDER_COMPLETED")
        finished_events = len(completed_orders)

        # 2. Next Event (date of the next event)
        # sort the events by date (field 'event_date'), and grab the next one
        next_event = orders.order_by("event_date").first()

        # 3. Last month's income (total of the last month in orders)
        last_month_orders = orders.filter(event_date__month=timezone.now().month)

        # TODO: change this calculation to account only for the percentage of
        # the musician; that is, discount the profit of Altempo as a platform
        last_month_income = sum(order.total for order in last_month_orders)

        # 4. Total Active Services
        active_services = music_project.services.filter(is_active=True)
        total_active_services = len(active_services)

        return Response(
            {
                "finished_events": finished_events,
                "next_event": next_event,
                "last_month_income": last_month_income,
                "total_active_services": total_active_services,
            }
        )


class RecommendationMusicProjectsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_projects = MusicProject.objects.order_by('-created_at')[:3]
        serializer = MusicProjectSerializer(last_projects, many=True)
        return Response(serializer.data)
