"""
Email sending utility for Altempo.

This module provides helper functions to send various types of emails
using Django's email system with i18n support.
"""

from typing import Any
from typing import Dict
from typing import Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _


class AltempoEmailSender:
    """Utility class for sending Altempo emails with i18n support."""

    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    SITE_NAME = "Altempo"

    # TODO: Configurar estas URLs en las settings del proyecto
    HELP_CENTER_URL = getattr(settings, "HELP_CENTER_URL", "https://altempo.dev/help")
    TERMS_URL = getattr(settings, "TERMS_URL", "https://altempo.dev/terms")
    PRIVACY_URL = getattr(settings, "PRIVACY_URL", "https://altempo.dev/privacy")
    INSTAGRAM_URL = getattr(settings, "INSTAGRAM_URL", "https://instagram.dev/altempo")
    LINKEDIN_URL = getattr(settings, "LINKEDIN_URL", "https://linkedin.dev/altempo")
    FACEBOOK_URL = getattr(settings, "FACEBOOK_URL", "https://facebook.dev/altempo")
    LOGO_URL = getattr(settings, "EMAIL_LOGO_URL", None)
    SITE_URL = getattr(settings, "SITE_URL", "https://altempo.dev")

    @classmethod
    def _send_email(
        cls,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        to_email: str,
        language: Optional[str] = None,
        from_email: Optional[str] = None,
    ) -> bool:
        """
        Internal method to send an email using a template.

        Args:
            subject: Email subject line
            template_name: Name of the template file (without path)
            context: Template context dictionary
            to_email: Recipient email address
            language: Language code for i18n (e.g., 'en', 'es')
            from_email: Sender email address (defaults to DEFAULT_FROM_EMAIL)

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        current_language = get_language()

        try:
            if language:
                activate(language)

            full_context = {
                **context,
                "help_center_url": cls.HELP_CENTER_URL,
                "terms_url": cls.TERMS_URL,
                "privacy_url": cls.PRIVACY_URL,
                "instagram_url": cls.INSTAGRAM_URL,
                "linkedin_url": cls.LINKEDIN_URL,
                "facebook_url": cls.FACEBOOK_URL,
                "site_url": cls.SITE_URL,
            }

            if cls.LOGO_URL:
                full_context["logo_url"] = cls.LOGO_URL
            elif hasattr(settings, "STATIC_URL") and settings.STATIC_URL:
                static_url = settings.STATIC_URL
                if static_url.startswith("http"):
                    full_context["logo_url"] = (
                        f"{static_url}images/email/altempo-logo.png"
                    )
                else:
                    base_url = cls.SITE_URL.rstrip("/")
                    static_path = static_url.rstrip("/")
                    full_context["logo_url"] = (
                        f"{base_url}{static_path}/images/email/altempo-logo.png"
                    )

            html_content = render_to_string(f"emails/{template_name}", full_context)

            email = EmailMultiAlternatives(
                subject=subject,
                body=html_content,  # Fallback plain text
                from_email=from_email or cls.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

        finally:
            activate(current_language)

    @classmethod
    def send_band_invitation_existing_user(
        cls,
        to_email: str,
        inviter_name: str,
        band_name: str,
        accept_url: str,
        decline_url: str,
        unsubscribe_url: str,
        expiry_days: int = 7,
        language: Optional[str] = None,
    ) -> bool:
        """
        Send band invitation email to an existing user.

        Args:
            to_email: Recipient's email address
            inviter_name: Name of the person sending the invitation
            band_name: Name of the band
            accept_url: URL to accept the invitation
            decline_url: URL to decline the invitation
            unsubscribe_url: URL to unsubscribe from emails
            expiry_days: Number of days until invitation expires
            language: Language code for i18n

        Returns:
            bool: True if email was sent successfully
        """
        subject = _("You've been invited to join %(band_name)s on Altempo") % {
            "band_name": band_name
        }

        context = {
            "inviter_name": inviter_name,
            "band_name": band_name,
            "accept_url": accept_url,
            "decline_url": decline_url,
            "unsubscribe_url": unsubscribe_url,
            "expiry_days": expiry_days,
        }

        return cls._send_email(
            subject=subject,
            template_name="band_invitation_existing_user.html",
            context=context,
            to_email=to_email,
            language=language,
        )

    @classmethod
    def send_band_invitation_new_user(
        cls,
        to_email: str,
        inviter_name: str,
        band_name: str,
        signup_url: str,
        unsubscribe_url: str,
        expiry_days: int = 7,
        language: Optional[str] = None,
    ) -> bool:
        """
        Send band invitation email to a new user (without an account).

        Args:
            to_email: Recipient's email address
            inviter_name: Name of the person sending the invitation
            band_name: Name of the band
            signup_url: URL to sign up and accept the invitation
            unsubscribe_url: URL to unsubscribe from emails
            expiry_days: Number of days until invitation expires
            language: Language code for i18n

        Returns:
            bool: True if email was sent successfully
        """
        subject = _("You've been invited to join %(band_name)s on Altempo") % {
            "band_name": band_name
        }

        context = {
            "inviter_name": inviter_name,
            "band_name": band_name,
            "signup_url": signup_url,
            "unsubscribe_url": unsubscribe_url,
            "expiry_days": expiry_days,
        }

        return cls._send_email(
            subject=subject,
            template_name="band_invitation_new_user.html",
            context=context,
            to_email=to_email,
            language=language,
        )

    @classmethod
    def send_email_verification(
        cls,
        to_email: str,
        user_name: str,
        verification_url: str,
        unsubscribe_url: str,
        expiry_hours: int = 24,
        language: Optional[str] = None,
    ) -> bool:
        """
        Send email verification email to a new user.

        Args:
            to_email: Recipient's email address
            user_name: User's name or username
            verification_url: URL to verify the email address
            unsubscribe_url: URL to unsubscribe from emails
            expiry_hours: Number of hours until verification link expires
            language: Language code for i18n

        Returns:
            bool: True if email was sent successfully
        """
        subject = _("Verify your Altempo account")

        context = {
            "user_name": user_name,
            "verification_url": verification_url,
            "unsubscribe_url": unsubscribe_url,
            "expiry_hours": expiry_hours,
        }

        return cls._send_email(
            subject=subject,
            template_name="email_verification.html",
            context=context,
            to_email=to_email,
            language=language,
        )

    @classmethod
    def send_email_verification_success(
        cls,
        to_email: str,
        user_name: str,
        dashboard_url: str,
        unsubscribe_url: str,
        language: Optional[str] = None,
    ) -> bool:
        """
        Send email verification success notification to user.

        Args:
            to_email: Recipient's email address
            user_name: User's name or username
            dashboard_url: URL to the user's dashboard
            unsubscribe_url: URL to unsubscribe from emails
            language: Language code for i18n

        Returns:
            bool: True if email was sent successfully
        """
        subject = _("Your Altempo account is verified!")

        context = {
            "user_name": user_name,
            "dashboard_url": dashboard_url,
            "unsubscribe_url": unsubscribe_url,
        }

        return cls._send_email(
            subject=subject,
            template_name="email_verification_success.html",
            context=context,
            to_email=to_email,
            language=language,
        )

    @classmethod
    def send_password_recovery(
        cls,
        to_email: str,
        user_name: str,
        reset_url: str,
        unsubscribe_url: str,
        expiry_hours: int = 1,
        language: Optional[str] = None,
    ) -> bool:
        """
        Send password recovery email to user.

        Args:
            to_email: Recipient's email address
            user_name: User's name or username
            reset_url: URL to reset the password
            unsubscribe_url: URL to unsubscribe from emails
            expiry_hours: Number of hours until reset link expires
            language: Language code for i18n

        Returns:
            bool: True if email was sent successfully
        """
        subject = _("Reset your Altempo password")

        context = {
            "user_name": user_name,
            "reset_url": reset_url,
            "unsubscribe_url": unsubscribe_url,
            "expiry_hours": expiry_hours,
        }

        return cls._send_email(
            subject=subject,
            template_name="password_recovery.html",
            context=context,
            to_email=to_email,
            language=language,
        )


# Convenience functions for easier importing
def send_band_invitation_existing_user(*args, **kwargs):
    """Convenience function for sending band invitation to existing user."""
    return AltempoEmailSender.send_band_invitation_existing_user(*args, **kwargs)


def send_band_invitation_new_user(*args, **kwargs):
    """Convenience function for sending band invitation to new user."""
    return AltempoEmailSender.send_band_invitation_new_user(*args, **kwargs)


def send_email_verification(*args, **kwargs):
    """Convenience function for sending email verification."""
    return AltempoEmailSender.send_email_verification(*args, **kwargs)


def send_email_verification_success(*args, **kwargs):
    """Convenience function for sending email verification success notification."""
    return AltempoEmailSender.send_email_verification_success(*args, **kwargs)


def send_password_recovery(*args, **kwargs):
    """Convenience function for sending password recovery email."""
    return AltempoEmailSender.send_password_recovery(*args, **kwargs)
