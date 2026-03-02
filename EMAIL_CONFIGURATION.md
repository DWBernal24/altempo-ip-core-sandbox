# Email Configuration for Altempo

## Issue Fixed
The `AnymailRequestsAPIError is not JSON serializable` error has been resolved by:
1. Adding proper ANYMAIL configuration in `local.py` settings
2. Converting exceptions to strings in error responses

## Required Environment Variables

Make sure your `.env` file contains these variables:

```bash
# Resend API Configuration
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# From Email (must be verified in Resend)
SENDGRID_FROM_EMAIL=noreply@altempo.dev
# OR if using a verified domain:
SENDGRID_FROM_EMAIL=Altempo <noreply@altempo.dev>

# Frontend URL for password reset links
FRONTEND_DEV_URL=http://localhost:3000
```

## Resend Setup Steps

1. **Get your API Key:**
   - Go to https://resend.com/api-keys
   - Create a new API key
   - Copy it to your `.env` file as `RESEND_API_KEY`

2. **Verify your domain or email:**
   - Go to https://resend.com/domains
   - Add and verify your domain (altempo.dev)
   - OR use a verified email address

3. **Set the FROM email:**
   - Use an email from your verified domain
   - Format: `noreply@altempo.dev` or `Altempo <noreply@altempo.dev>`

## Testing Email Sending

To test if emails are working:

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Test Email',
    message='This is a test',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-email@example.com'],
    fail_silently=False,
)
```

## Common Errors

### "AnymailRequestsAPIError: Resend API response 403"
- Your API key is invalid or missing
- Check that RESEND_API_KEY is set correctly

### "AnymailRequestsAPIError: Resend API response 400: from is required"
- SENDGRID_FROM_EMAIL is not set
- Add it to your .env file

### "AnymailRequestsAPIError: Resend API response 400: from must be verified"
- The email address in SENDGRID_FROM_EMAIL is not verified in Resend
- Verify your domain or email in the Resend dashboard

## Files Modified

1. `config/settings/local.py` - Added ANYMAIL configuration
2. `authentication/views.py` - Fixed exception serialization
3. All email templates - Updated with LinkedIn instead of Twitter

