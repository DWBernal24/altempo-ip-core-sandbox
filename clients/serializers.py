from rest_framework import serializers
from clients.models import UserProfileOnboardingDifficulty, ClientType, ClientDetail, ClientOnboardingDifficulty


class UserProfileOnboardingDifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileOnboardingDifficulty
        fields = ['difficulty', 'custom_description']


class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = '__all__'


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDetail
        fields = '__all__'


class ClientOnboardingDifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOnboardingDifficulty
        fields = '__all__'
