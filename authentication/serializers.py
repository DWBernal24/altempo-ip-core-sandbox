from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Language
from roles.models import UserProfile

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    # IDs from the items services endpoint (/api/items)
    id_services = serializers.ListField(child=serializers.IntegerField(required=False))
    id_role = serializers.IntegerField(read_only=True)
    id_country = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(required=False)
    id_referral_source = serializers.IntegerField(required=True)
    id_client_type = serializers.IntegerField(required=False)
    id_client_detail = serializers.IntegerField(required=False)
    other_client_detail = serializers.CharField(required=False)
    difficult_client = serializers.ListField(
        required=False, child=serializers.JSONField(required=False)
    )

    def validate_email(self, value):
        """
        Ensure email is unique across all users.
        """
        # Normalize email to lowercase for case-insensitive comparison
        email = value.lower()

        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )

        return email

    def custom_signup(self, request, user):
        user.name = self.validated_data.get("name", "")
        # user.is_active = False
        user.save()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"

    id = serializers.IntegerField()
    email = serializers.CharField()
    lastLoginAt = serializers.DateTimeField()
    verifiedAt = serializers.DateTimeField()
    isEnabled = serializers.BooleanField()
    isAvailable = serializers.BooleanField()
    createdAt = serializers.DateTimeField()
    updatedAt = serializers.DateTimeField()
    name = serializers.CharField()
    country = serializers.CharField()
    timezone = serializers.CharField()
    birthdate = serializers.DateTimeField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    howDidYouHearAboutUs = serializers.CharField()
    accountType = serializers.CharField()
    verified = serializers.BooleanField()


class GeneralProfileSerializer(serializers.ModelSerializer):
    language_code = serializers.SlugRelatedField(
        source="language", queryset=Language.objects.all(), slug_field="code"
    )
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileChangeLanguageSerializer(serializers.ModelSerializer):
    """
    Send the two-letter code of the language to assign it to the user's profile
    """

    language_code = serializers.SlugRelatedField(
        source="language", queryset=Language.objects.all(), slug_field="code"
    )

    class Meta:
        model = UserProfile
        fields = ["language_code"]
