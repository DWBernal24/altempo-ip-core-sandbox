# Email Invitation Setup Guide

## Overview

This document explains the changes made to adapt the invitation email templates to work with the Python server-side code.

## Changes Made

### 1. Python Code (`utils/band_invite.py`)

#### Added Context Variables

The following variables were added to the template context to match what the HTML templates expect:

- **`inviter_name`**: Full name or username of the person sending the invitation
- **`band_name`**: Name of the music project/band
- **`accept_link`**: URL to accept the invitation
- **`decline_link`**: URL to decline the invitation
- **`signup_link`**: URL for new users to sign up
- **`expiration_time`**: Human-readable expiration time (e.g., "48 hours")
- **Footer variables**: Social media links, legal links, current year, etc.

#### Updated Email Subject

Changed from a static Spanish subject to a dynamic, personalized one:
```python
subject = f"{inviter_name} te ha invitado a unirte a {band_name} en Altempo"
```

### 2. HTML Templates

#### Fixed Variable Syntax

Replaced markdown-style `**variable**` with proper Django template syntax:
- Changed `**{{ inviter_name }}**` to `<strong>{{ inviter_name }}</strong>`
- Changed `**{{ band_name }}**` to `{{ band_name }}` (already wrapped in styled span)
- Changed `**{{ expiration_time }}**` to `<strong>{{ expiration_time }}</strong>`
- Changed `**{{ current_year }}**` to `{{ current_year }}`

This was done in:
- `templates/emails/invitation_existing_user.html`
- `templates/emails/invitation_new_user.html`
- `templates/emails/altempo_footer.html`

## Configuration Required

### 1. Django Settings (`settings.py`)

Add the following settings to your Django configuration:

```python
# Email Configuration
DEFAULT_FROM_EMAIL = 'noreply@altempo.com'  # Update with your actual domain

# Social Media Links (optional)
INSTAGRAM_URL = 'https://instagram.com/altempo'
TWITTER_URL = 'https://twitter.com/altempo'
FACEBOOK_URL = 'https://facebook.com/altempo'
```

### 2. URL Configuration (`urls.py`)

Ensure you have the following URL patterns defined:

```python
urlpatterns = [
    # Invitation URLs
    path('invitations/accept/<uuid:invitation_id>/', accept_invitation_view, name='accept-invitation'),
    path('invitations/decline/<uuid:invitation_id>/', decline_invitation_view, name='decline-invitation'),
    
    # User URLs
    path('signup/', signup_view, name='signup'),
    
    # Footer URLs
    path('help/', help_center_view, name='help'),
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    path('unsubscribe/<str:email>/', unsubscribe_view, name='unsubscribe'),
]
```

### 3. Update Invitation Model

Ensure your invitation model has the following fields:

- `id`: UUID field
- `email`: Email address of the invitee
- `inviter`: ForeignKey to User (person sending the invitation)
- `invited_user`: ForeignKey to User (nullable, for existing users)
- `music_project`: ForeignKey to your MusicProject/Band model
- `expires_at`: DateTime field for expiration

### 4. Customize Expiration Time Logic

The current implementation uses a hardcoded "48 hours" string. You may want to calculate this dynamically:

```python
from django.utils import timezone
from datetime import timedelta

# In band_invite.py
time_diff = invitation.expires_at - timezone.now()
hours = int(time_diff.total_seconds() / 3600)

if hours < 24:
    expiration_time = f"{hours} horas"
elif hours < 48:
    expiration_time = "1 día"
else:
    days = hours // 24
    expiration_time = f"{days} días"
```

### 5. Update URL Paths

In `band_invite.py`, update the following URL paths to match your actual routes:

```python
# Line ~27: Signup URL
signup_url = request.build_absolute_uri("/signup/")

# Lines ~58-61: Footer links
"help_center_link": request.build_absolute_uri("/help/"),
"terms_link": request.build_absolute_uri("/terms/"),
"privacy_link": request.build_absolute_uri("/privacy/"),
"unsubscribe_link": request.build_absolute_uri(f"/unsubscribe/{invitation.email}/"),
```

### 6. Decline Invitation Endpoint (Optional)

If you want to support the decline functionality, create the view and update the URL:

```python
# In band_invite.py, update line ~19-23:
decline_url = request.build_absolute_uri(
    reverse("decline-invitation", kwargs={"invitation_id": str(invitation.id)})
)
```

Otherwise, you can remove the decline button from the template or leave it as "#".

## Testing

To test the email invitation system:

1. **Create a test invitation**:
   ```python
   from utils.band_invite import send_invitation_email
   
   send_invitation_email(invitation, request)
   ```

2. **Check email rendering** in Django console (development):
   - Emails will be printed to console if `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

3. **Test variables**:
   - Verify all variables render correctly
   - Check that links are absolute URLs
   - Ensure expiration time displays properly

## Email Client Compatibility Notes

The templates use Tailwind CSS via CDN. For better email client compatibility, consider:

1. **Inline CSS**: Use tools like `premailer` to inline all styles
2. **Remove External Fonts**: Some email clients block external resources
3. **Simplify Layout**: Complex flexbox might not work in older email clients
4. **Test Across Clients**: Use services like Litmus or Email on Acid

## Internationalization (i18n)

The templates use Django's `{% trans %}` and `{% blocktrans %}` tags for translation:

1. **Generate translation files**:
   ```bash
   python manage.py makemessages -l es
   python manage.py makemessages -l en
   ```

2. **Update translations** in `locale/es/LC_MESSAGES/django.po` and `locale/en/LC_MESSAGES/django.po`

3. **Compile translations**:
   ```bash
   python manage.py compilemessages
   ```

## Troubleshooting

### Variables not rendering

- Check that all context variables in `band_invite.py` match the template variables
- Verify the model has the required fields and relationships

### Links not working

- Ensure URL patterns are defined with correct names
- Check that `request` is properly passed to `send_invitation_email()`
- Verify `SITE_URL` or similar setting if using absolute URLs

### Emails not sending

- Check `EMAIL_BACKEND` configuration in settings
- Verify `DEFAULT_FROM_EMAIL` is set
- Check email server credentials (if using SMTP)

### Template not found

- Ensure template files are in `templates/emails/` directory
- Check `TEMPLATES['DIRS']` setting in Django configuration
- Verify `altempo_footer.html` exists in the same directory