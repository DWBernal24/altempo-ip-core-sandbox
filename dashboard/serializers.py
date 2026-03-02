from allauth.utils import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from services.models import Category
from musicians.models import MusicProject, MusicProjectVideoDraft, MusicProjectVideoDraftStatus

User = get_user_model()

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer that includes user data in the response.
    """

    def validate(self, attrs):
        # Get the user from credentials
        username = attrs.get('username')
        password = attrs.get('password')

        GENERIC_ERROR_MESSAGE = 'Invalid credentials.'

        user = authenticate(username=username, password=password)

        if user is None:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed(GENERIC_ERROR_MESSAGE)

        # Check if user account is active
        if not user.is_active:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed(GENERIC_ERROR_MESSAGE)

        # Check for UserProfile existence
        if not hasattr(user, 'profile'):
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed(GENERIC_ERROR_MESSAGE)

        # Import RoleChoices - adjust the import path to match your project!
        from roles.models import RoleChoices  # Update this import!

        # Check if user has admin role
        if user.profile.role.name != RoleChoices.ADMIN.value:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed(GENERIC_ERROR_MESSAGE)

        # Call parent's validate to generate tokens
        data = super().validate(attrs)

        # Add user data to response
        data['user'] = {
            'pk': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.name,
            'last_name': user.name,
        }

        return data


class LeanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "display_name"]


class LeanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class LeanMusicProjectSerializer(serializers.ModelSerializer):
    service_categories = LeanCategorySerializer(many=True, read_only=True)
    owner = LeanUserSerializer(read_only=True)

    class Meta:
        model = MusicProject
        fields = [
            "id",
            "name",
            "service_categories",
            "isProfileInfoCompleted",
            "isVerificationStepsCompleted",
            "isAvailabilityCompleted",
            "owner",
        ]


class ReviewMusicProjectVideoDraftSerializer(serializers.ModelSerializer):
    music_project = LeanMusicProjectSerializer(read_only=True)
    status = serializers.ChoiceField(choices=MusicProjectVideoDraftStatus.choices, required=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MusicProjectVideoDraft
        fields = [
            "id", "feedback", "reviewed_by", "reviewed_at", "status",
            "video_url", "caption", "music_project",
        ]
