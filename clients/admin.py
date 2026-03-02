from django.contrib import admin
from clients.models import ClientType, ClientDetail, ClientOnboardingDifficulty, UserProfileOnboardingDifficulty


@admin.register(ClientType)
class ClientTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ClientDetail)
class ClientDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_type', 'allows_custom_text')
    list_filter = ('client_type',)


@admin.register(ClientOnboardingDifficulty)
class ClientOnboardingDifficultyAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(UserProfileOnboardingDifficulty)
class UserProfileOnboardingDifficultyAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'difficulty')
