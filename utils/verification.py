import logging

from allauth.utils import get_user_model
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.profile.verified)


email_verification_token = EmailVerificationTokenGenerator()


def send_verification_email(user, request):
    """
    Send verification email to user using the new template system.

    Args:
        user: User object
        request: Request object for building absolute URLs
    """
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_url = request.build_absolute_uri(
        f"/api/auth/verify/user/{uid}/{token}",
    )

    logger.info("Sending verification email to user: %s", user.email)

    # Get user's display name
    user_name = user.username or "there"
    logger.info("User display name determined as: %s", user_name)

    # Verification links typically expire in 24 hours
    expiry_hours = 24

    # Get user's preferred language from profile
    language = None
    try:
        if hasattr(user, "profile") and user.profile and user.profile.language:
            language = user.profile.language.code.lower()
    except Exception:
        pass

    # Fallback to current language or English
    language = language or get_language() or "en"

    # Store current language to restore later
    current_language = get_language()

    try:
        # Activate user's preferred language
        activate(language)

        # Build context for the new template
        context = {
            "user_name": user_name,
            "verification_url": verification_url,
            "expiry_hours": expiry_hours,
            # Logo and site URLs
            "logo_url": getattr(settings, "EMAIL_LOGO_URL", None),
            "site_url": getattr(settings, "SITE_URL", "https://altempo.dev"),
            # Footer URLs
            "help_center_url": getattr(
                settings,
                "HELP_CENTER_URL",
                "https://altempo.dev/help",
            ),
            "terms_url": getattr(settings, "TERMS_URL", "https://altempo.dev/terms"),
            "privacy_url": getattr(
                settings,
                "PRIVACY_URL",
                "https://altempo.dev/privacy",
            ),
            "instagram_url": getattr(
                settings,
                "INSTAGRAM_URL",
                "https://instagram.dev/altempo",
            ),
            "linkedin_url": getattr(
                settings,
                "LINKEDIN_URL",
                "https://linkedin.dev/altempo",
            ),
            "facebook_url": getattr(
                settings,
                "FACEBOOK_URL",
                "https://facebook.dev/altempo",
            ),
            "unsubscribe_url": request.build_absolute_uri(
                f"/unsubscribe/{user.email}/",
            ),
        }

        # Build logo URL if not explicitly set
        if not context["logo_url"] and hasattr(settings, "STATIC_URL"):
            static_url = settings.STATIC_URL
            if static_url.startswith("http"):
                context["logo_url"] = f"{static_url}images/email/altempo-logo.png"
            else:
                base_url = context["site_url"].rstrip("/")
                static_path = static_url.rstrip("/")
                context["logo_url"] = (
                    f"{base_url}{static_path}/images/email/altempo-logo.png"
                )

        # Override with request-based URLs
        if request:
            context.update(
                {
                    "help_center_url": request.build_absolute_uri("/help/"),
                    "terms_url": request.build_absolute_uri("/terms/"),
                    "privacy_url": request.build_absolute_uri("/privacy/"),
                }
            )

        # Subject can be translated based on user's language
        subject = _("Verify your Altempo account, %(user_name)s") % {
            "user_name": user_name,
        }

        # Use the new template name
        html_message = render_to_string("emails/email_verification.html", context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info("Verification email sent successfully to: %s", user.email)

    finally:
        # Restore original language
        activate(current_language)


def send_verification_success_email(user, request):
    """
    Send verification success notification email to user.

    Args:
        user: User object
        request: Request object for building absolute URLs
    """
    logger.info("Sending verification success email to user: %s", user.email)

    # Get user's display name
    user_name = user.get_full_name() or user.username or "there"

    # Get user's preferred language from profile
    language = None
    try:
        if hasattr(user, "profile") and user.profile and user.profile.language:
            language = user.profile.language.code.lower()
    except Exception:
        pass

    # Fallback to current language or English
    language = language or get_language() or "en"

    # Store current language to restore later
    current_language = get_language()

    try:
        # Activate user's preferred language
        activate(language)

        # Build context for the new template
        context = {
            "user_name": user_name,
            "dashboard_url": request.build_absolute_uri("/dashboard/"),
            # Logo and site URLs
            "logo_url": getattr(settings, "EMAIL_LOGO_URL", None),
            "site_url": getattr(settings, "SITE_URL", "https://altempo.dev"),
            # Footer URLs
            "help_center_url": getattr(
                settings,
                "HELP_CENTER_URL",
                "https://altempo.dev/help",
            ),
            "terms_url": getattr(settings, "TERMS_URL", "https://altempo.dev/terms"),
            "privacy_url": getattr(
                settings,
                "PRIVACY_URL",
                "https://altempo.dev/privacy",
            ),
            "instagram_url": getattr(
                settings,
                "INSTAGRAM_URL",
                "https://instagram.dev/altempo",
            ),
            "linkedin_url": getattr(
                settings,
                "LINKEDIN_URL",
                "https://linkedin.dev/altempo",
            ),
            "facebook_url": getattr(
                settings,
                "FACEBOOK_URL",
                "https://facebook.dev/altempo",
            ),
            "unsubscribe_url": request.build_absolute_uri(
                f"/unsubscribe/{user.email}/",
            ),
        }

        # Build logo URL if not explicitly set
        if not context["logo_url"] and hasattr(settings, "STATIC_URL"):
            static_url = settings.STATIC_URL
            if static_url.startswith("http"):
                context["logo_url"] = f"{static_url}images/email/altempo-logo.png"
            else:
                base_url = context["site_url"].rstrip("/")
                static_path = static_url.rstrip("/")
                context["logo_url"] = (
                    f"{base_url}{static_path}/images/email/altempo-logo.png"
                )

        # Override with request-based URLs
        if request:
            context.update(
                {
                    "help_center_url": request.build_absolute_uri("/help/"),
                    "terms_url": request.build_absolute_uri("/terms/"),
                    "privacy_url": request.build_absolute_uri("/privacy/"),
                    "dashboard_url": request.build_absolute_uri("/dashboard/"),
                }
            )

        subject = _("Your Altempo account is verified, %(user_name)s!") % {
            "user_name": user_name,
        }
        html_message = render_to_string(
            "emails/email_verification_success.html", context
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info("Verification success email sent successfully to: %s", user.email)

    finally:
        # Restore original language
        activate(current_language)


def verify_token(uidb64, token):
    """
    Verify the token that was sent to the user.

    Args:
        uidb64: Base64 encoded user ID
        token: Verification token

    Returns:
        User object if token is valid, None otherwise
    """

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return None

    if email_verification_token.check_token(user, token):
        return user

    return None
