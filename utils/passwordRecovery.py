import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def send_password_recovery_email(user, recovery_url, request=None):
    """
    Send password recovery email to user using the new template system.

    Args:
        user: User object
        recovery_url: URL for password reset
        request: Optional request object for building absolute URLs
    """
    logger.info("Sending password recovery email to user: %s", user.email)

    # Get user's display name
    user_name = user.username

    # Password reset links typically expire in 1 hour
    expiry_hours = 1

    # Get user's preferred language from profile
    if user.profile.language is not None:
        language = user.profile.language.code.lower()
    else:
        language = "en"

    # Store current language to restore later
    current_language = get_language()

    try:
        # Activate user's preferred language
        activate(language)

        # Build context for the new template
        context = {
            "user_name": user_name,
            "reset_url": recovery_url,
            "expiry_hours": expiry_hours,
            # Logo and site URLs
            "logo_url": getattr(settings, "EMAIL_LOGO_URL", None),
            "site_url": getattr(settings, "SITE_URL", "https://altempo.dev"),
            # Footer URLs
            "help_center_url": getattr(
                settings, "HELP_CENTER_URL", "https://altempo.dev/help"
            ),
            "terms_url": getattr(settings, "TERMS_URL", "https://altempo.dev/terms"),
            "privacy_url": getattr(
                settings, "PRIVACY_URL", "https://altempo.dev/privacy"
            ),
            "instagram_url": getattr(
                settings, "INSTAGRAM_URL", "https://instagram.dev/altempo"
            ),
            "linkedin_url": getattr(
                settings, "LINKEDIN_URL", "https://linkedin.dev/altempo"
            ),
            "facebook_url": getattr(
                settings, "FACEBOOK_URL", "https://facebook.dev/altempo"
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

        # Add request-dependent URLs if request is available
        if request:
            context.update(
                {
                    "help_center_url": request.build_absolute_uri("/help/"),
                    "terms_url": request.build_absolute_uri("/terms/"),
                    "privacy_url": request.build_absolute_uri("/privacy/"),
                    "unsubscribe_url": request.build_absolute_uri(
                        f"/unsubscribe/{user.email}/",
                    ),
                },
            )
        else:
            # Use default or settings-based unsubscribe URL
            context["unsubscribe_url"] = getattr(
                settings,
                "UNSUBSCRIBE_URL",
                f"https://altempo.dev/unsubscribe/{user.email}/",
            )

        # Subject can be translated based on user's language
        subject = _("Reset your Altempo password, %(user_name)s") % {
            "user_name": user_name
        }

        # Use the new template name
        html_message = render_to_string("emails/password_recovery.html", context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info("Password recovery email sent successfully to: %s", user.email)

    finally:
        # Restore original language
        activate(current_language)
