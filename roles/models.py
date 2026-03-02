import enum
from zoneinfo import available_timezones
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from clients.models import ClientType, ClientDetail
from services.models import Category, Item
from core.models import Country, ReferralSource, Gender, MusicalGenreTag, Language, Instrument
from musicians.utils import dynamic_upload_path

User = get_user_model()

class RoleChoices(enum.Enum):
    MUSICIAN = 'MUSICIAN'
    TALENT_HUNTER = 'TALENT_HUNTER'
    STUDENT = 'STUDENT'
    ADMIN = 'ADMIN'


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='roles/', blank=True, null=True)

    def __str__(self):
        return self.name


# validation for IANA type strings when modifying timezone
def validate_timezone(value):
    """Validate that the timezone is a valid IANA timezone"""
    if value not in available_timezones():
        raise ValidationError(f'{value} is not a valid IANA timezone')


class UserProfile(models.Model):
    from utils.get_default_language import get_default_language

    class UserProfileStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING_REVIEW = 'pending_review', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    client_type = models.ForeignKey(ClientType, on_delete=models.SET_NULL, null=True, blank=True)
    client_detail = models.ForeignKey(ClientDetail, on_delete=models.SET_NULL, null=True, blank=True)
    custom_client_detail = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    referral_source = models.ForeignKey(ReferralSource, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=UserProfileStatus.choices,
        default=UserProfileStatus.DRAFT
    )
    verified = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.SET_DEFAULT, default=get_default_language)

    # Timezone
    # for both customers (talent hunters) and musicians
    timezone = models.CharField(max_length=255, blank=True, null=True, default="UTC", validators=[validate_timezone])

    # campos especificos para el talent hunter

    #identidad del talent hunter
    role_company = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True)
    subcategories = models.ManyToManyField(Item, blank=True)

    # Presupuesto y condiciones
    MODALTY_CHOICES = [
        ('ones', 'One-off (único evento)'),
        ('mensual_supscription', 'Suscripción mensual'),
        ('quarterly', 'Paquete trimestrales'),
        ('annual', 'Paquetes anuales'),
    ]
    contracting_modalty = models.CharField(choices= MODALTY_CHOICES, max_length=255, blank=True, null=True)

    #localidad y logistica
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    # frecuencia y agenda
    FRECUENCY_CHOICES = [
        ('ones', 'Unico (one-shot)'),
        ('mensual', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('biannual', 'Semestral'),
        ('annual', 'Anual'),
    ]
    frecuency = models.CharField(choices= FRECUENCY_CHOICES, max_length=255, blank=True, null=True)


    def __str__(self):
        return f"Profile {self.user.username}"

class Demografy(models.Model):
    name = models.CharField(max_length=255)
    other = models.BooleanField(default=False)
    def __str__(self):
        return f"Demografia {self.name}"

class ListDemografyProfile(models.Model):
    demografy = models.ForeignKey(Demografy, on_delete=models.CASCADE, related_name="demografyprofile")
    is_other = models.BooleanField(default=False)
    other_name = models.CharField(max_length=255, null=True, blank=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

class KeyDates(models.Model):
    name = models.CharField(max_length=255)
    other = models.BooleanField(default=False)

class KeyDatesProfile(models.Model):
    key_dates = models.ForeignKey(KeyDates, on_delete=models.CASCADE, related_name="keydatesprofile")
    is_other = models.BooleanField(default=False)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

class UserCategory(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = ('user_profile', 'category')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.category.name} ({self.status})"

class Gallery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)

class Album(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="album")
    name = models.TextField()
    link = models.TextField()
    STATUS_TYPE = (
        ('YOUTUBE', 'Youtube'),
        ('SPOTIFY', 'Spotify'),
        ('OTHER', 'Otro'),
    )
    type = models.CharField(choices=STATUS_TYPE, max_length=100)


