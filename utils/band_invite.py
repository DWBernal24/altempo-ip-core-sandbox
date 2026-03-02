import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def send_invitation_email(invitation, invitation_token, request):
    """
    Send invitation email with options for accepting or declining the invitation.
    Uses the new template system.

    Args:
        invitation: Invitation object
        request: Request object for building absolute URLs
    """

    accept_url = (
        request.build_absolute_uri(
            reverse(
                "accept-invitation",
                kwargs={
                    "invitation_id": str(invitation.id),
                    "token": invitation_token,
                },
            ),
        )
        + "?action=accept"
    )

    decline_url = (
        request.build_absolute_uri(
            reverse(
                "decline-invitation",
                kwargs={
                    "invitation_id": str(invitation.id),
                    "token": invitation_token,
                },
            ),
        )
        if hasattr(settings, "DECLINE_INVITATION_URL")
        else "#"
    ) + "?action=decline"

    signup_url = "https://altempo.dev/signup"

    is_existing_user = invitation.invited_user is not None
    logger.info("Sending invitation from user: %s", request.user)

    expiry_days = 7

    inviter_name = invitation.inviter.username
    band_name = invitation.music_project.name

    language = None
    if is_existing_user and invitation.invited_user:
        if invitation.invited_user.profile:
            if invitation.invited_user.profile.language is not None:
                language = invitation.invited_user.profile.language.code.lower()
            else:
                language = "en"

    language = language or get_language() or "en"
    current_language = get_language()

    try:
        activate(language)

        context = {
            "inviter_name": inviter_name,
            "band_name": band_name,
            "expiry_days": expiry_days,
            # Logoand site URLs
            "logo_url": getattr(settings, "EMAIL_LOGO_URL", None),
            "site_url": getattr(settings, "SITE_URL", "https://altempo.dev"),
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
            "unsubscribe_url": request.build_absolute_uri(
                f"/unsubscribe/{invitation.email}/",
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

        # Add template-specific URLs
        if is_existing_user:
            context.update(
                {
                    "accept_url": accept_url,
                    "decline_url": decline_url,
                }
            )
        else:
            context.update(
                {
                    "signup_url": signup_url,
                }
            )

        if request:
            context.update(
                {
                    "help_center_url": request.build_absolute_uri("/help/"),
                    "terms_url": request.build_absolute_uri("/terms/"),
                    "privacy_url": request.build_absolute_uri("/privacy/"),
                }
            )

        template_name = (
            "emails/band_invitation_existing_user.html"
            if is_existing_user
            else "emails/band_invitation_new_user.html"
        )

        subject = _(
            "%(inviter_name)s has invited you to join %(band_name)s on Altempo"
        ) % {
            "inviter_name": inviter_name,
            "band_name": band_name,
        }
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
            fail_silently=False,
        )

        logger.info(
            "Invitation email sent successfully to: %s (existing_user=%s)",
            invitation.email,
            is_existing_user,
        )

    finally:
        activate(current_language)
