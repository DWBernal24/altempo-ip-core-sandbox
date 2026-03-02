from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from authentication.views import CheckVerifiedAPIView, CustomMusicianRegisterView, CustomStudentRegisterView, CustomTalentHunterRegisterView, GoogleLogin, CustomPasswordResetView, CustomPasswordResetConfirmView, ProfileView, UserProfileChangeLanguageView, VerifyAccountAPIView, SendEmailVerifyAPIView

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

urlpatterns = [
    # path("register/", RegisterView.as_view(), name="rest_register"),

    # old registratoin route
    # path("register/", CustomRegisterView.as_view(), name='rest_register'),

    path("register/musician/", CustomMusicianRegisterView.as_view(), name='musician_rest_register'),
    path("register/talent-hunter/", CustomTalentHunterRegisterView.as_view(), name='talent_hunter_rest_register'),
    path("register/student/", CustomStudentRegisterView.as_view(), name='student_rest_register'),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile_user"),
    path("profile/language/", UserProfileChangeLanguageView.as_view(), name="profile_user_update_language"),
    path("verify/user/<uidb64>/<token>/", VerifyAccountAPIView.as_view(), name="verify_account"),
    path("profile/<int:pk>/checkVerified/", CheckVerifiedAPIView.as_view(), name="profile_check_verified"),
    path("verify/send/", SendEmailVerifyAPIView.as_view(), name="send-verify"),

    # ---- Password recovery ----
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # ---- GOOGLE AUTH ----
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
