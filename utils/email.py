import logging
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import DynamicTemplateData
from sendgrid.helpers.mail import From
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


def send_template_email(to_email, template_id, dynamic_data, send_copy=True):
    """
    Envía un correo usando una plantilla dinámica de SendGrid.

    Args:
        send_copy (bool): Send copy
        to_email (str): Email del destinatario.
        template_id (str): ID de la plantilla dinámica de SendGrid.
        dynamic_data (dict): Diccionario con los datos dinámicos para la plantilla.
    """
    to_emails = [to_email]

    if send_copy:
        to_emails.append(os.environ.get("SENDGRID_ORDER_EXTRA_EMAIL"))

    message = Mail(
        from_email=From(
            os.environ.get("SENDGRID_FROM_EMAIL"),
            os.environ.get("SENDGRID_COMPANY_NAME"),
        ),
        to_emails=to_emails,
    )

    message.template_id = template_id
    message.dynamic_template_data = dynamic_data

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"SendGrid error: {e}")
        return None


def send_email_basic(to_email, subject, content):
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.RESEND_SMTP_PORT,
        username=settings.RESEND_SMTP_USERNAME,
        password=os.environ.get("RESEND_API_KEY"),
        use_tls=True,
    ) as connection:
        r = EmailMessage(
            subject=subject,
            body=content,
            to=[to_email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            connection=connection,
        ).send()


def send_wishlist_email(user, request=None):
    """
    Send wishlist confirmation email to student users.

    Args:
        user: User object who joined the student wishlist
        request: Optional request object for building absolute URLs
    """
    logger.info("Sending wishlist email to student user: %s", user.email)

    # Get user's display name
    user_name = user.username
    if hasattr(user, "profile") and user.profile and user.profile.name:
        user_name = user.profile.name

    # Get user's preferred language from profile
    language = "en"
    if hasattr(user, "profile") and user.profile and user.profile.language is not None:
        language = user.profile.language.code.lower()

    # Store current language to restore later
    current_language = get_language()

    try:
        # Activate user's preferred language
        activate(language)

        # Build context for the template
        context = {
            "user_name": user_name,
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
                settings, "INSTAGRAM_URL", "https://instagram.com/altempo.app/"
            ),
            "linkedin_url": getattr(
                settings, "LINKEDIN_URL", "https://linkedin.com/company/altempoapp/"
            ),
            "facebook_url": getattr(
                settings, "FACEBOOK_URL", "https://facebook.com/atempoapp"
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
        subject = _("Welcome to Altempo - You're on the Wishlist! 🎓")

        # Render the template
        html_message = render_to_string("emails/student_wishlist.html", context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info("Wishlist email sent successfully to: %s", user.email)

    finally:
        # Restore original language
        activate(current_language)
