import uuid
from django.contrib.auth import get_user_model
from rest_framework import serializers
from slugify import slugify
from roles.models import Role, UserProfile, UserCategory, Demografy, ListDemografyProfile, KeyDates, KeyDatesProfile
from musicians.serializers import ProfileMusicProjectSerializer, MusicProjectSerializer
from musicians.models import MusicProjectType, MusicProject
from clients.models import UserProfileOnboardingDifficulty
from clients.serializers import UserProfileOnboardingDifficultySerializer

User = get_user_model()


class DemografySerializer(serializers.ModelSerializer):
    class Meta:
        model = Demografy
        fields = '__all__'

class ListDeListDemografyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListDemografyProfile
        fields = '__all__'

class ListDeListDemografyProfileExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListDemografyProfile
        fields = '__all__'
        depth = 1

class KeyDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyDates
        fields = '__all__'

class KeyDatesProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyDatesProfile
        fields = '__all__'

class KeyDatesProfileExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyDatesProfile
        fields = '__all__'
        depth = 1

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ['category']


class UserProfileSerializer(serializers.ModelSerializer):
    music_project = ProfileMusicProjectSerializer(many=True, required=False)
    user_categories = UserCategorySerializer(many=True, required=True)
    client_onboarding_difficulties = UserProfileOnboardingDifficultySerializer(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)

        if data.get('role').name == 'MUSICIAN':
            # TODO: Check the implementation to support multiple categories
            # Right now is only checking and validating for AMBIENT_MUSIC type of service
            # (which, btw, is already outdated, since the new row in the datbase is called MUSIC_SETTING)
            # Check Category
            user_categories_data = data.get('user_categories', [])
            curr_categories = ["MUSIC_SETTING", "MUSIC_LEARNING", "MUSIC_MARKETING", "MUSIC_THERAPY"]

            # check categories
            for category in user_categories_data:
                if category.get('category').name not in curr_categories:
                    raise serializers.ValidationError(f"Category {category.get('category').name} is not valid")

            music_project_type = data.get("music_project", {}).get("project_type", None)

            # TODO: Validate these requirements, do not all of the musicians should have a music project?
            if not music_project_type: # ID: 1 - INVIDUAL, ID: 2 - GROUP
                raise serializers.ValidationError("Music project type is required for ambient music service")

        if data.get('role').name in ['TALENT_HUNTER', "STUDENT"]:
            if not data.get('client_type'):
                raise serializers.ValidationError("Client type is required for talent hunters and students")

            if not data.get('client_detail'):
                raise serializers.ValidationError("Client detail is required for talent hunters and students")

        return data

    def create(self, validated_data):
        # Pop additional data
        music_project = validated_data.pop("music_project", {})
        user_categories_data = validated_data.pop('user_categories', [])
        difficulties_data = validated_data.pop("client_onboarding_difficulties", [])
        user = validated_data.pop("user")

        profile, created = UserProfile.objects.update_or_create(user=user, defaults=validated_data)

        # Check if role is musician
        if validated_data.get('role').name == 'MUSICIAN':  # TODO add constants

            # Get project type
            if not music_project.get("project_type"):
                music_project["project_type"] = MusicProjectType.objects.get(name="INDIVIDUAL")

            # Create default music project
            music_project_data = {
                "name": f"{user.name} music project",
                "slug": slugify(f"{user.name} music project {str(uuid.uuid4())[:8]}"),
                "project_type": music_project.get("project_type").id,
                "owner": user.id,
                "birth_date" : profile.birth_date,
            }

            # Valdate MusicProjectSerializer
            music_project_serializer = MusicProjectSerializer(data=music_project_data)

            if music_project_serializer.is_valid():
                music_project_serializer.save()
            else:
                raise serializers.ValidationError(music_project_serializer.errors)

            # Create user categories
            for category_data in user_categories_data:
                UserCategory.objects.create(user_profile=profile, **category_data)


        # Check if role is client:
        if validated_data.get('role').name in ['TALENT_HUNTER', "STUDENT"]: # TODO add constants

            # Create user categories
            for category_data in user_categories_data:
                UserCategory.objects.create(user_profile=profile, status=UserCategory.APPROVED, **category_data)

            # Create UserProfileOnboardingDifficulty
            for difficulty_data in difficulties_data:
                UserProfileOnboardingDifficulty.objects.create(user_profile=profile, **difficulty_data)

        return profile


class UserProfileGetSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'role', 'client_type', 'client_detail', 'custom_client_detail',
            'country', 'birth_date', 'gender', 'phone_number', 'referral_source'
        ]
