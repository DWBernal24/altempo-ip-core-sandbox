# Student Wishlist Email Integration

## Overview
A new email template and function have been created to notify students that they've been added to the wishlist while the student features are being developed.

## Files Created/Modified

### 1. New Email Template
**Location:** `templates/emails/student_wishlist.html`

Features:
- ✨ Beautiful, branded design matching other Altempo emails
- 🎓 Student-focused messaging
- 📋 Feature highlights (Connect with Musicians, Learning Resources, Student Projects)
- 🌍 Multi-language support via Django i18n
- 📱 Responsive design for all devices

### 2. New Email Function
**Location:** `utils/email.py`
**Function:** `send_wishlist_email(user, request=None)`

Features:
- Sends wishlist confirmation email
- Supports internationalization (uses user's preferred language)
- Automatically builds all necessary URLs
- Includes proper error handling and logging

## How to Use

### In Your Student Registration View

Update your `CustomStudentRegisterView` in `authentication/views.py`:

```python
from utils.email import send_wishlist_email

class CustomStudentRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        # ... your existing registration code ...
        
        # After creating the user profile
        profile.save()

        # Send wishlist email instead of verification email
        try:
            send_wishlist_email(user, request)
        except Exception as e:
            logger.error(f"Failed to send wishlist email: {str(e)}")
            # Optionally: still return success but log the error
            # Don't delete the user - they're on the wishlist!
            
        return Response(
            {
                "detail": "You've been added to the student wishlist! Check your email.",
                "user": user_data,
            },
            status=status.HTTP_201_CREATED,
        )
```

### Alternative: Send Later

If you want to send the wishlist email at a different time:

```python
from utils.email import send_wishlist_email
from django.contrib.auth import get_user_model

User = get_user_model()

# Send to a specific user
user = User.objects.get(email='student@example.com')
send_wishlist_email(user)

# Send to all students on wishlist
students = User.objects.filter(profile__role__name='STUDENT')
for student in students:
    try:
        send_wishlist_email(student)
    except Exception as e:
        logger.error(f"Failed to send to {student.email}: {str(e)}")
```

## Testing

### Test in Django Shell

```python
from django.contrib.auth import get_user_model
from utils.email import send_wishlist_email

User = get_user_model()
user = User.objects.get(email='your-test-email@example.com')

# Send test email
send_wishlist_email(user)
```

### Test via API

Make a student registration request and check:
1. User receives the wishlist email
2. Email renders correctly in email client
3. All links work properly
4. Correct language is used (if user has language preference)

## Email Preview

The email includes:
- 🎓 Friendly welcome message
- 💜 Purple-branded wishlist confirmation box
- ✅ Three key features with icons:
  - 🎵 Connect with Musicians
  - 📚 Learning Resources
  - 🎸 Student Projects
- 📧 All standard footer links (Help, Terms, Privacy, Social Media)

## Customization

### Change the Features List

Edit `templates/emails/student_wishlist.html` and modify the feature sections around line 40-90.

### Adjust Email Subject

Edit `utils/email.py`, line 156:
```python
subject = _("Welcome to Altempo - You're on the Wishlist! 🎓")
```

### Add More Context Variables

In `utils/email.py`, add to the `context` dictionary (around line 99):
```python
context = {
    "user_name": user_name,
    "your_custom_variable": "your_value",
    # ... existing variables
}
```

Then use in the template:
```django
{{ your_custom_variable }}
```

## Translations

To add translations for different languages:

1. Extract translatable strings:
```bash
python manage.py makemessages -l es
python manage.py makemessages -l fr
```

2. Edit the `.po` files in `locale/` directory

3. Compile messages:
```bash
python manage.py compilemessages
```

## Troubleshooting

### Email Not Sending

1. Check RESEND_API_KEY is set in .env
2. Check DEFAULT_FROM_EMAIL is verified in Resend
3. Check logs: `logger.error` messages in console

### Wrong Language

The function uses the user's profile language. Make sure:
- User profile has `language` field set
- Language code exists and is valid (e.g., 'en', 'es', 'fr')

### Template Not Found

Ensure the template exists at:
`templates/emails/student_wishlist.html`

## Future Enhancements

When student features are ready:
1. Create a new "Student Platform Ready" email template
2. Send to all wishlisted students
3. Include login link and feature overview

```python
# Future function
def send_student_platform_ready_email(user, request=None):
    # Notify students that platform is ready
    pass
```
