from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class ReferralSource(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class MusicalGenreTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InstrumentType(models.Model):
    class InstrumentTypeChoices(models.TextChoices):
        MUSICAL_INSTRUMENTS = "musical_instruments", "Instrumentos Musicales"
        AMPLIFY_AND_SOUND = "amplify_and_sound", "Amplificación y Sonido"
        LIGHTNING = "illumination", "Iluminación"
        VIDEO_AND_SCREENS = "video_and_screens", "Video y Pantallas"
        SCENARIO_AND_STRUCTURE = "scenario_and_structure", "Escenario y Estructura"
        ENERGY_AND_CABLES = "energy_and_cables", "Energía y Cables"
        SCENOGRAPHY = "scenography", "Escenografía"
        PRODUCTION_AND_LOGISTICS = "production_and_logistics", "Producción y Logística"
        COMMUNICATION_AND_CONTROL = (
            "communication_and_control",
            "Comunicación y Control",
        )
        AMBIANCE_AND_VISUALS = "ambiance_and_visuals", "Ambiente y Visuales"
        STREAMING_AND_RECORDING = "streaming_and_recording", "Streaming y Grabación"
        SECURITY = "security", "Seguridad"
        TRANSPORT_AND_STORAGE = "transport_and_storage", "Transporte y Almacenamiento"

    name = models.CharField(
        max_length=100, choices=InstrumentTypeChoices.choices, unique=True
    )
    display_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(InstrumentType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        InstrumentCategory, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name


class MusicianVoiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class VocalStyle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class CollabType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class DJType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    inventory = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to="core/equipment/", blank=True, null=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    PROFILE_COMPLETED = "PROFILE_COMPLETED"
    BRIEF_INITIATED = "BRIEF_INITIATED"
    BRIEF_VALIDATED = "BRIEF_VALIDATED"
    OBJECTIVE_SCORE_READY = "OBJECTIVE_SCORE_READY"
    PLAN_SONORO_CREATED = "PLAN_SONORO_CREATED"
    TALENT_RECOMMENDED = "TALENT_RECOMMENDED"
    SCOUTING_INITIATED = "SCOUTING_INITIATED"
    STRATEGY_ADJUSTMENT_REQUESTED = "STRATEGY_ADJUSTMENT_REQUESTED"
    TALENT_AVAILABILITY_CONFIRMED = "TALENT_AVAILABILITY_CONFIRMED"
    CONTINUOUS_PLAN_OFFERED = "CONTINUOUS_PLAN_OFFERED"
    MUSICIANS_CONFIRMED = "MUSICIANS_CONFIRMED"
    CONTINGENCY_PLAN_READY = "CONTINGENCY_PLAN_READY"
    PROGRESS_TRACKING_ACTIVE = "PROGRESS_TRACKING_ACTIVE"
    EVENT_REMINDER_SENT = "EVENT_REMINDER_SENT"
    POST_EVENT_SURVEY_SENT = "POST_EVENT_SURVEY_SENT"
    EVENT_RESULTS_READY = "EVENT_RESULTS_READY"
    BENCHMARKING_READY = "BENCHMARKING_READY"
    CONTINUOUS_PLAN_READY = "CONTINUOUS_PLAN_READY"
    ROI_RECOMMENDATIONS_READY = "ROI_RECOMMENDATIONS_READY"
    SUBSCRIPTION_UPSELL = "SUBSCRIPTION_UPSELL"
    INVITE_BAND_MEMBER = "INVITE_BAND_MEMBER"
    INVITE_BAND_CONFIRMED = "INVITE_BAND_CONFIRMED"
    INVITE_BAND_DECLINED = "INVITE_BAND_DECLINED"
    VIDEO_APPROVED = "VIDEO_APPROVED"
    VIDEO_REJECTED = "VIDEO_REJECTED"

    title = models.CharField(max_length=250)

    # deprecated field, kept for backward compatibility
    # since translations are done in the frontend, this field is no longer used
    message = models.TextField()  # a short message, to keep the UI simple

    TYPES_NOTIFICATION_CHOICES = [
        # tipo de notificaciones de talent hunter
        (PROFILE_COMPLETED, "Completar perfil"),
        (BRIEF_INITIATED, "Completar briefing"),
        (BRIEF_VALIDATED, "Ver diagnóstico"),
        (OBJECTIVE_SCORE_READY, "Mejorar objetivo"),
        (PLAN_SONORO_CREATED, "Ver plan sonoro"),
        (TALENT_RECOMMENDED, "Ver recomendaciones"),
        (SCOUTING_INITIATED, "Ver scouting"),
        (STRATEGY_ADJUSTMENT_REQUESTED, "Ajustar estrategia"),
        (TALENT_AVAILABILITY_CONFIRMED, "Confirmar selección"),
        (CONTINUOUS_PLAN_OFFERED, "Agendar próximas sesiones"),
        (MUSICIANS_CONFIRMED, "Revisar scouting"),
        (CONTINGENCY_PLAN_READY, "Ver plan de respaldo"),
        (PROGRESS_TRACKING_ACTIVE, "Ver progreso"),
        (EVENT_REMINDER_SENT, "Ver detalle"),
        (POST_EVENT_SURVEY_SENT, "Enviar feedback"),
        (EVENT_RESULTS_READY, "Ver resultados"),
        (BENCHMARKING_READY, "Ver comparativa"),
        (ROI_RECOMMENDATIONS_READY, "Ver mejoras sugeridas"),
        (SUBSCRIPTION_UPSELL, "Mejorar con datos"),
        (INVITE_BAND_MEMBER, "Invitación a banda"),
        (INVITE_BAND_CONFIRMED, "Invitación a banda confirmada"),
        (INVITE_BAND_DECLINED, "Invitación a banda rechazada"),
        (VIDEO_APPROVED, "Video aprobado"),
        (VIDEO_REJECTED, "Video rechazado"),
    ]
    type = models.CharField(max_length=180, choices=TYPES_NOTIFICATION_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notification"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    # este campo se usa para almacenar cualquier valor para su redireccionamiento.
    redirect_link = models.TextField()

    # this field contains all the values that will be parsed by the frontend
    # leaving this here for translation purposes,
    # since translation is done in the frontend
    values = models.JSONField(null=True, blank=True)

    # this represents a larger message with more text, in case that is needed
    # the UI is already adapted to handle notifications with larger text as details
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.title
