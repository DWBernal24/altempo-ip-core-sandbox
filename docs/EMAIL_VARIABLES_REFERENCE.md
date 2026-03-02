# Email Template Variables Reference

## Quick Reference Guide

This document provides a quick reference for all variables used in the invitation email templates and their sources.

## Template Variables Mapping

### Common Variables (Both Templates)

| Variable Name | Source | Type | Description | Example |
|--------------|--------|------|-------------|---------|
| `inviter_name` | `invitation.inviter.get_full_name()` or `invitation.inviter.username` | String | Full name of person sending invitation | "John Doe" |
| `band_name` | `invitation.music_project.name` | String | Name of the band/music project | "The Rockers" |
| `expiration_time` | Calculated from `invitation.expires_at` | String | Human-readable expiration time | "48 hours", "2 days" |
| `invitation` | Direct model instance | Object | Full invitation object | - |
| `music_project` | `invitation.music_project` | Object | Full music project object | - |
| `inviter` | `invitation.inviter` | Object | Full inviter user object | - |
| `is_existing_user` | `invitation.invited_user is not None` | Boolean | Whether invitee has account | `True`/`False` |
| `expires_at` | `invitation.expires_at` | DateTime | Raw expiration datetime | - |

### Existing User Template (`invitation_existing_user.html`)

| Variable Name | Source | Type | Description | Example |
|--------------|--------|------|-------------|---------|
| `accept_link` | `reverse('accept-invitation', ...)` | String | URL to accept invitation | "https://altempo.com/invitations/accept/123..." |
| `decline_link` | `reverse('decline-invitation', ...)` | String | URL to decline invitation | "https://altempo.com/invitations/decline/123..." |

### New User Template (`invitation_new_user.html`)

| Variable Name | Source | Type | Description | Example |
|--------------|--------|------|-------------|---------|
| `signup_link` | `request.build_absolute_uri("/signup/")` | String | URL to signup page | "https://altempo.com/signup/" |

### Footer Variables (`altempo_footer.html`)

| Variable Name | Source | Type | Description | Example |
|--------------|--------|------|-------------|---------|
| `current_year` | `now().year` | Integer | Current year | 2024 |
| `instagram_link` | `settings.INSTAGRAM_URL` | String | Instagram profile URL | "https://instagram.com/altempo" |
| `twitter_link` | `settings.TWITTER_URL` | String | Twitter/X profile URL | "https://twitter.com/altempo" |
| `facebook_link` | `settings.FACEBOOK_URL` | String | Facebook profile URL | "https://facebook.com/altempo" |
| `help_center_link` | `request.build_absolute_uri("/help/")` | String | Help center URL | "https://altempo.com/help/" |
| `terms_link` | `request.build_absolute_uri("/terms/")` | String | Terms of service URL | "https://altempo.com/terms/" |
| `privacy_link` | `request.build_absolute_uri("/privacy/")` | String | Privacy policy URL | "https://altempo.com/privacy/" |
| `unsubscribe_link` | `request.build_absolute_uri(...)` | String | Unsubscribe URL | "https://altempo.com/unsubscribe/user@example.com/" |

## Template Usage Examples

### Using Variables in Django Templates

```html
<!-- Simple variable -->
<p>Hello, {{ inviter_name }}!</p>

<!-- Variable with translation -->
<h1>{% trans "Welcome" %}</h1>

<!-- Variable with blocktrans (for sentences with variables) -->
<p>
  {% blocktrans with inviter_name=inviter_name band_name=band_name %}
    <strong>{{ inviter_name }}</strong> has invited you to join {{ band_name }}.
  {% endblocktrans %}
</p>

<!-- Using as link href -->
<a href="{{ accept_link }}">Accept Invitation</a>

<!-- Conditional rendering -->
{% if is_existing_user %}
  <p>Welcome back!</p>
{% else %}
  <p>Create an account to get started.</p>
{% endif %}
```

## Context Building in Python

### Location
`altempo_core_service/utils/band_invite.py` - `send_invitation_email()` function

### Example Context Dictionary

```python
context = {
    # User & Project Info
    "inviter_name": "John Doe",
    "band_name": "The Rockers",
    
    # URLs
    "accept_link": "https://altempo.com/invitations/accept/abc-123",
    "decline_link": "https://altempo.com/invitations/decline/abc-123",
    "signup_link": "https://altempo.com/signup/",
    
    # Timing
    "expiration_time": "48 hours",
    "expires_at": datetime(2024, 1, 15, 12, 0, 0),
    
    # Model Objects
    "invitation": <Invitation object>,
    "music_project": <MusicProject object>,
    "inviter": <User object>,
    
    # Flags
    "is_existing_user": True,
    
    # Footer
    "current_year": 2024,
    "instagram_link": "https://instagram.com/altempo",
    "twitter_link": "https://twitter.com/altempo",
    "facebook_link": "https://facebook.com/altempo",
    "help_center_link": "https://altempo.com/help/",
    "terms_link": "https://altempo.com/terms/",
    "privacy_link": "https://altempo.com/privacy/",
    "unsubscribe_link": "https://altempo.com/unsubscribe/user@example.com/",
}
```

## Customization Tips

### Adding New Variables

1. **Update Python context** in `band_invite.py`:
   ```python
   context = {
       # ... existing variables ...
       "your_new_variable": "some value",
   }
   ```

2. **Use in template**:
   ```html
   <p>{{ your_new_variable }}</p>
   ```

### Dynamic Expiration Time Calculation

Replace hardcoded `"48 hours"` with:

```python
from django.utils import timezone
from datetime import timedelta

time_diff = invitation.expires_at - timezone.now()
hours = int(time_diff.total_seconds() / 3600)

if hours < 1:
    expiration_time = "menos de 1 hora"
elif hours == 1:
    expiration_time = "1 hora"
elif hours < 24:
    expiration_time = f"{hours} horas"
elif hours < 48:
    expiration_time = "1 día"
else:
    days = hours // 24
    expiration_time = f"{days} días"
```

### Adding User Profile Picture

1. **Add to context**:
   ```python
   "inviter_avatar_url": invitation.inviter.profile.avatar.url if invitation.inviter.profile.avatar else None,
   ```

2. **Use in template**:
   ```html
   {% if inviter_avatar_url %}
     <img src="{{ inviter_avatar_url }}" alt="Avatar">
   {% else %}
     <span class="material-symbols-outlined">account_circle</span>
   {% endif %}
   ```

## Translation Notes

All user-facing text should use Django's i18n tags:

- **`{% trans "Simple text" %}`** - For simple strings without variables
- **`{% blocktrans %}Text with {{ variable }}{% endblocktrans %}`** - For text with variables
- **`{% blocktrans with var1=var1 var2=var2 %}`** - Explicitly pass variables to blocktrans

### Example

```html
<!-- WRONG -->
<p>{{ inviter_name }} invited you to {{ band_name }}</p>

<!-- RIGHT -->
<p>
  {% blocktrans with inviter_name=inviter_name band_name=band_name %}
    {{ inviter_name }} invited you to {{ band_name }}
  {% endblocktrans %}
</p>
```

## Debugging Checklist

- [ ] Variable name matches between Python context and template
- [ ] Variable is properly escaped in template (`{{ }}` for values, `{% %}` for tags)
- [ ] All `blocktrans` variables are declared with `with var=var`
- [ ] URL names match between `reverse()` calls and `urls.py`
- [ ] Model relationships exist (e.g., `invitation.music_project` is not None)
- [ ] Settings variables are defined (e.g., `INSTAGRAM_URL`)
- [ ] Request object is passed correctly to `send_invitation_email()`

## Common Issues

### Issue: Variable shows as empty or "None"
**Solution**: Check that the model instance has that field populated. Add fallback:
```python
"inviter_name": invitation.inviter.get_full_name() or invitation.inviter.username or "Someone"
```

### Issue: URL shows as relative path
**Solution**: Use `request.build_absolute_uri()` for all URLs in emails:
```python
accept_url = request.build_absolute_uri(reverse('accept-invitation', ...))
```

### Issue: Expiration time in wrong language
**Solution**: Use Django's timezone and translation utilities:
```python
from django.utils.translation import gettext as _
expiration_time = _("48 hours")
```
