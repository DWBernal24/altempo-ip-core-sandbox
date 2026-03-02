from django.db import models


class ClientType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='clients/client_types/', blank=True, null=True)

    def __str__(self):
        return self.name


class ClientDetail(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default="", blank=True)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE, related_name="details")
    allows_custom_text = models.BooleanField(default=False)
    image = models.ImageField(upload_to='clients/client_detail/', blank=True, null=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.client_type.name} - {self.name}"


class ClientOnboardingDifficulty(models.Model):
    from roles.models import Role

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="client_difficulties")
    type = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField()
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.role.name} - {self.description}"


class UserProfileOnboardingDifficulty(models.Model):
    from roles.models import UserProfile

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="client_onboarding_difficulties")
    difficulty = models.ForeignKey(ClientOnboardingDifficulty, on_delete=models.CASCADE)
    custom_description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user_profile', 'difficulty')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.difficulty.description}"
