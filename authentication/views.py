import datetime
import os

from allauth.account.forms import ResetPasswordForm
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.base import logger
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework import status
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from clients.models import ClientDetail
from clients.models import ClientOnboardingDifficulty
from clients.models import ClientType
from clients.models import UserProfileOnboardingDifficulty
from core.models import Country, Language
from core.models import ReferralSource
from core.serializers import LanguageSerializer
from musicians.models import InviteMemberBand
from musicians.models import MusicProject
from musicians.serializers import InviteMemberBandSerializer
from musicians.serializers import MusicProjectSerializer
from roles.models import Role
from roles.models import RoleChoices
from roles.models import UserProfile
from roles.serializers import CustomUserDetailSerializer
from services.serializers import CategorySerializer
from services.serializers import ItemSerializer
from utils.email import send_email_basic
from utils.email import send_wishlist_email
from utils.passwordRecovery import send_password_recovery_email
from utils.verification import send_verification_email
from utils.verification import verify_token

from .serializers import CustomRegisterSerializer, UserProfileChangeLanguageSerializer
from .serializers import GeneralProfileSerializer
from .serializers import ProfileSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get("GOOGLE_CALL_BACK_URL")
    client_class = OAuth2Client


class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        from django.utils.translation import gettext as _

        form = ResetPasswordForm(data=request.data)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_user_model().objects.get(email__iexact=email, is_active=True)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{os.environ.get('FRONTEND_DEV_URL')}/reset-password?uid={uid}&token={token}"

            try:
                send_password_recovery_email(user, reset_url, request)
            except Exception as e:
                logger.error(f"Failed to send password recovery email: {str(e)}")
                return Response(
                    {
                        "message": _("Password reset e-mail has not been sent."),
                        "detail": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )


class CustomPasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password1 = request.data.get("password")
        password2 = request.data.get("passwordConfirmation")

        if not uid or not token or not password1 or not password2:
            return Response(
                {"detail": "All the fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password1 != password2:
            return Response(
                {"detail": "The passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response(
                {"detail": "Invalid UID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password1)
        user.save()

        return Response(
            {"detail": "The password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


# @method_decorator(csrf_exempt, name='dispatch')
# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = self.perform_create(serializer)
#         role = Role.objects.get(id=request.data['id_role'])
#
#         if role.name == "TALENT_HUNTER":
#             if  not request.data.get('id_client_type'):
#                 return JsonResponse({"id_client_type": ["This field is required."]}, status=400)
#             if not request.data.get('id_client_detail'):
#                 return JsonResponse({"id_client_detail": ["This field is required."]}, status=400)
#
#         # Serializar usuario con el campo "name"
#         user_data = CustomUserDetailSerializer(user).data
#         country = Country.objects.get(id=request.data.get('id_country'))
#         referral_source = ReferralSource.objects.get(id=request.data.get('id_referral_source'))
#         # Validando si es cliente Talent_hunter
#         if role.name == "TALENT_HUNTER":
#             client_type = ClientType.objects.get(id = request.data.get('id_client_type'))
#             client_detail = ClientDetail.objects.get(id = request.data.get('id_client_detail'))
#             difficulties = request.data.get('difficult_client')
#             if not client_type:
#                 return JsonResponse({"id_client_type": ["This field is required."]}, status=400)
#
#             if not client_detail:
#                 return JsonResponse({"id_client_detail": ["This field is required."]}, status=400)
#
#             if client_detail.name == "Otros" and not request.data.get('other_client_detail'):
#                 return JsonResponse({"other_client_detail": ["This field is required."]}, status=400)
#
#             if not difficulties:
#                 return JsonResponse({"difficult_client": ["This field is required."]}, status=400)
#
#             profile = UserProfile(
#                 user=user,
#                 role=role,
#                 country=country,
#                 phone_number=request.data.get('phone_number'),
#                 referral_source=referral_source,
#                 client_type=client_type,
#                 client_detail=client_detail,
#                 custom_client_detail=request.data.get('other_client_detail'),
#                 birth_date=request.data.get('birth_date'),
#                 name=request.data.get('name')
#             )
#             profile.save()
#
#             if len(difficulties) > 0:
#                 for difficulty in difficulties:
#                     onboarding = ClientOnboardingDifficulty.objects.get(id=difficulty.get('id'))
#                     if onboarding:
#                         user_profile_onboarding = UserProfileOnboardingDifficulty(
#                             user_profile=profile,
#                             difficulty=onboarding,
#                             custom_description=difficulty.get('custom_description')
#                         )
#                         user_profile_onboarding.save()
#
#         else:
#             profile = UserProfile(
#                 user=user,
#                 role=role,
#                 country=country,
#                 phone_number=request.data.get('phone_number'),
#                 referral_source=referral_source,
#                 birth_date=request.data.get('birth_date'),
#                 name=request.data.get('name'),
#             )
#             profile.save()
#
#         # creando token de verificación
#         try:
#             send_verification_email(user, request)
#         except Exception as e:
#             # TODO test the behavior of deleting a user. Does it actually delete all the information?
#             user.delete()
#             print(str(e))
#             return Response({
#                 'error': 'Failed to send verification email. Please, try again',
#                 'details': str(e),
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         # Generar JWT
#         refresh = RefreshToken.for_user(user)
#
#         if role.name == "MUSICIAN":
#             # send information about the pending invitations to other bands
#             return Response({
#                 'user': user_data,
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'detail': 'Registro exitoso',
#                 'pending_invitations': InviteMemberBandSerializer(
#                     InviteMemberBand.objects.filter(
#                         email=user.email,
#                         status=InviteMemberBand.STATUS_CHOICES[2][0]
#                     ).all(),
#                     many=True
#                 ).data
#             })
#
#         return Response({
#             'user': user_data,
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'detail': 'Registro exitoso',
#         })
#
#     def perform_create(self, serializer):
#         return serializer.save(self.request)


@method_decorator(csrf_exempt, name="dispatch")
class CustomMusicianRegisterView(RegisterView):
    """
    This endpoint assumes that only Musician-type users will be registering.
    Music-project information is created separately (in the /music-project/ endpoint)
    """

    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        user_data = CustomUserDetailSerializer(user).data
        country = Country.objects.get(id=request.data.get("id_country"))
        referral_source = ReferralSource.objects.get(
            id=request.data.get("id_referral_source")
        )

        profile = UserProfile(
            user=user,
            role=Role.objects.get(name=RoleChoices.MUSICIAN.value),
            country=country,
            phone_number=request.data.get("phone_number"),
            referral_source=referral_source,
            birth_date=request.data.get("birth_date"),
            name=request.data.get("name"),
            language=Language.objects.get(code=request.data.get("language_code")),
        )
        profile.save()

        # Send verification email
        try:
            send_verification_email(user, request)
        except Exception as e:
            # TODO test the behavior of deleting a user. Does it actually delete all the information?
            user.delete()
            print(str(e))
            return Response(
                {
                    "error": "Failed to send verification email. Please, try again",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        refresh = RefreshToken.for_user(user)

        # send information about the pending invitations to other bands
        return Response(
            {
                "user": user_data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "detail": "Registro exitoso",
                "pending_invitations": InviteMemberBandSerializer(
                    InviteMemberBand.objects.filter(
                        email=user.email, status=InviteMemberBand.STATUS_CHOICES[2][0]
                    ).all(),
                    many=True,
                ).data,
            }
        )

    def perform_create(self, serializer):
        return serializer.save(self.request)


@method_decorator(csrf_exempt, name="dispatch")
class CustomTalentHunterRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        if not request.data.get("id_client_type"):
            return JsonResponse(
                {"id_client_type": ["This field is required."]}, status=400
            )
        if not request.data.get("id_client_detail"):
            return JsonResponse(
                {"id_client_detail": ["This field is required."]}, status=400
            )

        # Serializar usuario con el campo "name"
        user_data = CustomUserDetailSerializer(user).data
        country = Country.objects.get(id=request.data.get("id_country"))
        referral_source = ReferralSource.objects.get(
            id=request.data.get("id_referral_source")
        )
        # Validando si es cliente Talent_hunter
        client_type = ClientType.objects.get(id=request.data.get("id_client_type"))
        client_detail = ClientDetail.objects.get(
            id=request.data.get("id_client_detail")
        )
        difficulties = request.data.get("difficult_client")
        if not client_type:
            return JsonResponse(
                {"id_client_type": ["This field is required."]}, status=400
            )

        if not client_detail:
            return JsonResponse(
                {"id_client_detail": ["This field is required."]}, status=400
            )

        if client_detail.name == "Otros" and not request.data.get(
            "other_client_detail"
        ):
            return JsonResponse(
                {"other_client_detail": ["This field is required."]}, status=400
            )

        if not difficulties:
            return JsonResponse(
                {"difficult_client": ["This field is required."]}, status=400
            )

        profile = UserProfile(
            user=user,
            role=Role.objects.get(name=RoleChoices.TALENT_HUNTER.value),
            country=country,
            phone_number=request.data.get("phone_number"),
            referral_source=referral_source,
            client_type=client_type,
            client_detail=client_detail,
            custom_client_detail=request.data.get("other_client_detail"),
            birth_date=request.data.get("birth_date"),
            name=request.data.get("name"),
        )
        profile.save()

        if len(difficulties) > 0:
            for difficulty in difficulties:
                onboarding = ClientOnboardingDifficulty.objects.get(
                    id=difficulty.get("id")
                )
                if onboarding:
                    user_profile_onboarding = UserProfileOnboardingDifficulty(
                        user_profile=profile,
                        difficulty=onboarding,
                        custom_description=difficulty.get("custom_description"),
                    )
                    user_profile_onboarding.save()

        try:
            send_verification_email(user, request)
        except Exception as e:
            # TODO test the behavior of deleting a user. Does it actually delete all the information?
            user.delete()
            print(str(e))
            return Response(
                {
                    "error": "Failed to send verification email. Please, try again",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Generar JWT
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": user_data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "detail": "Registro exitoso",
            }
        )

    def perform_create(self, serializer):
        return serializer.save(self.request)


@method_decorator(csrf_exempt, name="dispatch")
class CustomStudentRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        if not request.data.get("id_client_type"):
            return JsonResponse(
                {"id_client_type": ["This field is required."]}, status=400
            )
        if not request.data.get("id_client_detail"):
            return JsonResponse(
                {"id_client_detail": ["This field is required."]}, status=400
            )

        user_data = CustomUserDetailSerializer(user).data
        country = Country.objects.get(id=request.data.get("id_country"))
        referral_source = ReferralSource.objects.get(
            id=request.data.get("id_referral_source")
        )
        client_type = ClientType.objects.get(id=request.data.get("id_client_type"))
        client_detail = ClientDetail.objects.get(
            id=request.data.get("id_client_detail")
        )

        if client_detail.name == "Otros" and not request.data.get(
            "other_client_detail"
        ):
            return JsonResponse(
                {"other_client_detail": ["This field is required."]}, status=400
            )

        profile = UserProfile(
            user=user,
            role=Role.objects.get(name=RoleChoices.TALENT_HUNTER.value),
            country=country,
            phone_number=request.data.get("phone_number"),
            referral_source=referral_source,
            client_type=client_type,
            client_detail=client_detail,
            custom_client_detail=request.data.get("other_client_detail"),
            birth_date=request.data.get("birth_date"),
            name=request.data.get("name"),
        )
        profile.save()

        try:
            send_wishlist_email(user, request)
        except Exception as e:
            # TODO test the behavior of deleting a user. Does it actually delete all the information?
            user.delete()
            print(str(e))
            return Response(
                {
                    "error": "Failed to send wishlist email. Please, try again",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Generar JWT
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": user_data,
                "wishlisted": True,
                "detail": "Registro exitoso",
                "access": str(refresh.access_token),
            }
        )

    def perform_create(self, serializer):
        return serializer.save(self.request)


class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        user_profile = UserProfile.objects.get(user=user)
        
        gender = str(user_profile.gender) if user_profile.gender is not None else None
        role = user_profile.role

        music_project = MusicProject.objects.filter(owner=user.id).all()
        member_music_projects = user.member_projects.all()

        serializer_music = None
        serializer_member_music_projects = None

        if music_project:
            serializer_music = MusicProjectSerializer(instance=music_project, many=True)
            serializer_member_music_projects = MusicProjectSerializer(
                instance=member_music_projects, many=True
            )

        if serializer_music:
            data_music_project = serializer_music.data
        else:
            data_music_project = []

        if serializer_member_music_projects:
            data_member_music_projects = serializer_member_music_projects.data
        else:
            data_member_music_projects = []

        category_serializer = None
        if user_profile.category:
            category_serializer = CategorySerializer(instance=user_profile.category)

        subcategories_serializer = []
        if user_profile.subcategories:
            subcategories_serializer = ItemSerializer(
                instance=user_profile.subcategories, many=True
            )

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "username": user.get_username(),
                "lastLoginAt": datetime.datetime(2025, 5, 22),
                "verifiedAt": datetime.datetime(2025, 5, 22),
                "isEnabled": True,
                "isAvailable": True,
                "createdAt": datetime.datetime(2025, 5, 22),
                "updatedAt": datetime.datetime(2025, 5, 22),
                "name": user_profile.name if user_profile.name else user.name,
                "country": 303,
                "timezone": user_profile.timezone,
                "birthdate": datetime.datetime(
                    user_profile.birth_date.year,
                    user_profile.birth_date.month,
                    user_profile.birth_date.day,
                ),
                "gender": gender,
                "language": user_profile.language.id if user_profile.language else 1,
                "phone": user_profile.phone_number,
                "howDidYouHearAboutUs": "Redes sociales",
                "accountType": role.name,
                "verified": user_profile.verified,
                "music_project": data_music_project + data_member_music_projects,
                "role_company": user_profile.role_company,
                "category": category_serializer.data if category_serializer else None,
                "subcategories": subcategories_serializer.data
                if subcategories_serializer
                else [],
                "contracting_modalty": user_profile.contracting_modalty,
                "address": user_profile.address,
                "city": user_profile.city,
                "frecuency": user_profile.frecuency,
            }
        )

    def patch(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        user_profile = UserProfile.objects.get(user=user)

        # change the email associated with the user if present
        if request.data.get("email") and request.data.get("email") != user.email:
            user.email = request.data.get("email")
            user.save()

            # verification process back to false
            user_profile.verified = False
            user_profile.save()

        serializer = GeneralProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileChangeLanguageView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileChangeLanguageSerializer(
            user_profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para verificación de usuario
class VerifyAccountAPIView(APIView):
    def get(self, request, uidb64, token):
        from django.conf import settings
        from django.utils.timezone import now
        from django.utils.translation import activate
        from django.utils.translation import get_language
        from django.utils.translation import gettext as _

        user = verify_token(uidb64, token)

        context = {
            "success": False,
            "already_verified": False,
            "error_message": None,
            "user": None,
            "app_link": getattr(settings, "APP_URL", "/"),
            # Footer variables
            "current_year": now().year,
            "instagram_link": getattr(settings, "INSTAGRAM_URL", "#"),
            "linkedin_link": getattr(settings, "LINKEDIN_URL", "#"),
            "facebook_link": getattr(settings, "FACEBOOK_URL", "#"),
            "help_center_link": request.build_absolute_uri("/help/"),
            "terms_link": request.build_absolute_uri("/terms/"),
            "privacy_link": request.build_absolute_uri("/privacy/"),
            "unsubscribe_link": "#",
        }

        if user is not None:
            current_language = get_language()

            if user.profile.language is not None:
                user_language = user.profile.language.code.lower()
            else:
                user_language = "en"

            logger.info(f"User language: {user_language}")
            if current_language != user_language:
                activate(user_language)

        if user is None:
            context["error_message"] = _(
                "The verification link is invalid or has expired."
            )
            return render(request, "emails/email_verification_error.html", context)

        if user.profile.verified:
            context["already_verified"] = True
            context["user"] = user
            return render(request, "emails/email_verification_success.html", context)

        user.profile.verified = True
        user.profile.save()

        context["success"] = True
        context["user"] = user

        return render(request, "emails/email_verification_success.html", context)


class SendEmailVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = get_user_model().objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=user)
        if not profile.verified:
            send_verification_email(user, request)
            return Response({"send": True, "verify": False})
        else:
            return Response({"send": False, "verify": True})


class CheckVerifiedAPIView(APIView):
    def get(self, request, pk):
        user = get_user_model().objects.get(id=pk)
        return Response({"verified": user.profile.verified}, status=status.HTTP_200_OK)

