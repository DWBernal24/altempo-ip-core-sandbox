"""
Email Logo Configuration Example

Add these settings to your Django settings file to configure the logo
that appears in email templates.

Copy the relevant section to:
- config/settings/base.py (for settings used everywhere)
- config/settings/local.py (for development)
- config/settings/production.py (for production)
"""

# =============================================================================
# EMAIL LOGO & BRANDING CONFIGURATION
# =============================================================================

# Main site URL - used for links in emails
# This should be the base URL of your application
SITE_URL = env("SITE_URL", default="https://altempo.dev")

# Email logo URL - the full absolute URL to your logo image
# This MUST be an absolute URL (starting with https://) for emails to work
EMAIL_LOGO_URL = env("EMAIL_LOGO_URL", default=None)

# If EMAIL_LOGO_URL is not set, the templates will automatically try to
# construct it from STATIC_URL + SITE_URL + 'images/email/altempo-logo.png'

# Additional branding URLs (already configured in base.py, shown here for reference)
HELP_CENTER_URL = env("HELP_CENTER_URL", default=f"{SITE_URL}/help")
TERMS_URL = env("TERMS_URL", default=f"{SITE_URL}/terms")
PRIVACY_URL = env("PRIVACY_URL", default=f"{SITE_URL}/privacy")
INSTAGRAM_URL = env("INSTAGRAM_URL", default="https://www.instagram.com/altempo.app/")
LINKEDIN_URL = env(
    "LINKEDIN_URL", default="https://www.linkedin.com/company/altempoapp/"
)
FACEBOOK_URL = env("FACEBOOK_URL", default="https://www.facebook.com/atempoapp")


# =============================================================================
# EXAMPLE CONFIGURATIONS FOR DIFFERENT ENVIRONMENTS
# =============================================================================

# -----------------------------------------------------------------------------
# LOCAL DEVELOPMENT EXAMPLE
# -----------------------------------------------------------------------------
# For local development, you can use a placeholder or local file
# (Note: local files won't work when actually sending emails)
#
# EMAIL_LOGO_URL = 'https://via.placeholder.com/200x50/7605e1/ffffff?text=Altempo'
# SITE_URL = 'http://localhost:8000'

# -----------------------------------------------------------------------------
# PRODUCTION WITH AWS S3 EXAMPLE
# -----------------------------------------------------------------------------
# If you're using S3 for static files (already configured in production.py):
#
# aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# STATIC_URL = f"https://{aws_s3_domain}/static/"
# EMAIL_LOGO_URL = f"{STATIC_URL}images/email/altempo-logo.png"
# SITE_URL = env('SITE_URL', default='https://altempo.com')

# -----------------------------------------------------------------------------
# PRODUCTION WITH CDN EXAMPLE
# -----------------------------------------------------------------------------
# If you're using a CDN for static files:
#
# EMAIL_LOGO_URL = 'https://cdn.altempo.com/images/email/altempo-logo.png'
# SITE_URL = 'https://altempo.com'

# -----------------------------------------------------------------------------
# PRODUCTION WITH DIRECT URL EXAMPLE
# -----------------------------------------------------------------------------
# If you're hosting the logo on your own server:
#
# EMAIL_LOGO_URL = 'https://altempo.com/static/images/email/altempo-logo.png'
# SITE_URL = 'https://altempo.com'


# =============================================================================
# ENVIRONMENT VARIABLES (.env file)
# =============================================================================
# You can also set these via environment variables:
#
# Add to your .env file:
# SITE_URL=https://altempo.com
# EMAIL_LOGO_URL=https://cdn.altempo.com/images/email/altempo-logo.png
#
# Then in settings:
# SITE_URL = env('SITE_URL', default='https://altempo.com')
# EMAIL_LOGO_URL = env('EMAIL_LOGO_URL', default=None)


# =============================================================================
# TESTING YOUR CONFIGURATION
# =============================================================================
# After adding these settings, test them:
#
# 1. In Django shell:
#    python manage.py shell
#    >>> from django.conf import settings
#    >>> print(settings.EMAIL_LOGO_URL)
#    >>> print(settings.SITE_URL)
#
# 2. Send test email:
#    python manage.py test_email_templates --email your@email.com
#
# 3. Check the email in your inbox to verify the logo appears


# =============================================================================
# IMPORTANT NOTES
# =============================================================================
# 1. EMAIL_LOGO_URL MUST be an absolute URL (https://...)
# 2. The logo file should be accessible publicly (not behind authentication)
# 3. Recommended logo size: 200x50px (PNG or JPG)
# 4. Keep file size under 50KB for fast email loading
# 5. If EMAIL_LOGO_URL is not set, emails will show "♪ Altempo" text instead
# 6. The logo path in static files should be: static/images/email/altempo-logo.png
