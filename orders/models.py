from django.db import models
from django.utils.timezone import now
from services.models import ServiceMode, Item, SpecificService, Attribute
from musicians.models import CategoryMusic
from core.models import (
    ReferralSource,
    MusicalGenreTag,
    VocalStyle,
    Instrument,
    CollabType,
    MusicianVoiceType,
    DJType,
    Equipment,
)


class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    allow_custom_message = models.BooleanField(default=False)
    image = models.ImageField(upload_to='orders/event_types/', blank=True, null=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CustomerLifecycle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class EventGoal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    allow_custom_message = models.BooleanField(default=False)
    customer_lifecycle = models.ForeignKey(CustomerLifecycle, on_delete=models.SET_NULL, null=True, blank=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class MusicAmbianceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='orders/music_ambiance_type/', blank=True, null=True)

    def __str__(self):
        return self.name


class EventVisit(models.Model):
    PENDING = 'pending'
    APPROVED = 'visited'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Visited')
    ]

    visit_date = models.DateField()
    visit_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)


class SoundPackage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class OrderServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='orders/service_types/', blank=True, null=True)

    def __str__(self):
        return self.name

class OrderTemplate(models.Model):
    name = models.CharField(unique=True, max_length=200)
    idea = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.PositiveIntegerField(blank=True, null=True)  # just if is more than 4 hours
    modality = models.ForeignKey(ServiceMode, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='orders/order_template/', blank=True, null=True)
    ambiance_type = models.ForeignKey(MusicAmbianceType, on_delete=models.SET_NULL, null=True, blank=True)
    # genres
    music_genre_tags = models.ManyToManyField(MusicalGenreTag, blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    TECHNICAL_LEVEL_CHOICES = [
        ('medium', 'Medio'),
        ('proffesional', 'Profesional')
    ]
    technical_level = models.CharField(choices=TECHNICAL_LEVEL_CHOICES, blank=True, null=True, max_length=60)
    logistics = models.BooleanField(default=False)
    personalization = models.TextField(blank=True, null=True)
    price = models.FloatField()
    FEATURED_TAG_CHOICES = [
        ('popular', 'Popular'),
        ('new', 'Nuevo'),
        ('promotion', 'En promoción'),
        ('recommended', 'Recomendado'),
        ('top', 'Top local'),
    ]
    featured_tag = models.CharField(choices=FEATURED_TAG_CHOICES, blank=True, null=True, max_length=60)
    cta_label_1 = models.CharField(blank=True, null=True)
    cta_label_2 = models.CharField(blank=True, null=True)


class Order(models.Model):
    from roles.models import UserProfile
    from musicians.models import MusicProject, CategoryMusic

    order_number = models.CharField(max_length=20, unique=True, blank=True)

    # order template
    order_template = models.ForeignKey(OrderTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    # Event type -> social event
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    event_type_custom_message = models.TextField(blank=True, null=True)

    # event_goal + customer lifecycle
    event_goal = models.ForeignKey(EventGoal, on_delete=models.SET_NULL, null=True, blank=True)
    event_goal_custom_message = models.TextField(blank=True, null=True)

    # ambience type -> energy
    ambiance_type = models.ForeignKey(MusicAmbianceType, on_delete=models.SET_NULL, null=True, blank=True)

    # genres
    music_genre_tags = models.ManyToManyField(MusicalGenreTag, blank=True)

    STATUS_TYPE_CHOICES = [
        ('CONCEPT_DEFINED', 'Cliente definio concepto'),
        ('MUSICIANS_SELECTED', 'Musico seleccionado'),
        ('SCOUTING_INITIATED', 'Inicio acounting en el lugar'),
        ('LOGISTICS_PROPOSAL_SENT', 'Envio de propuesta de lógistica'),
        ('LOGISTICS_PROPOSAL_ACCEPTED', 'Cliente acepto la propuesta de logistica'),
        ('LOGISTICS_PROPOSAL_REJECTED', 'Cliente rechazo la propuesta de logistica'),
        ('ORDER_CONFIRMED', 'Cliente confirmo la orden'),
        ('CHECKLIST_IN_PROGRESS', 'Orden en proceso'),
        ('EVENT_EXECUTING', 'Evento siendo ejecutado'),
        ('ORDER_COMPLETED', 'Orden completado'),
        ('ORDER_CANCELLED', 'Orden cancelado'),
        ('POST_EVENT_FEEDBACK_PENDING', 'Pendiente de recibir feedback'),
        ('POST_EVENT_FEEDBACK_RECEIVED', 'Feedback recibido')
    ]
    status = models.CharField(choices=STATUS_TYPE_CHOICES, blank=True, null=True, max_length=100)

    # specific requirements
    has_specific_requirements = models.BooleanField(default=False)
    specific_requirements = models.TextField(blank=True, null=True)

    # edad estimada del publico
    estimated_age = models.IntegerField(blank=True, null=True)

    # perfil del beneficiario
    profile_beneficiary = models.TextField(blank=True, null=True)

    # Service type -> music / lights
    service_type = models.ForeignKey(OrderServiceType, on_delete=models.SET_NULL, null=True, blank=True)

    # Item -> category
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)

    # collab type
    collab_type = models.ForeignKey(CollabType, on_delete=models.SET_NULL, null=True, blank=True)

    # ---- Event information ----

    # on site / virtual
    modality = models.ForeignKey(ServiceMode, on_delete=models.SET_NULL, null=True, blank=True)

    event_city = models.TextField(blank=True, null=True)
    event_address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    VENUE_TYPE_CHOICES = [
        ('indoor', 'Espacio cerrado'),
        ('outdoor', 'Al aire libre')
    ]
    venue_type = models.CharField(choices=VENUE_TYPE_CHOICES, blank=True, null=True, max_length=10)

    PATH_CHOICES = [
        ('blank', 'En blanco'),
        ('artist', 'Seleccionando artista'),
        ('template', 'Por plantilla'),
        ('band', 'Banda'),
        ('soundequipment', 'Equipo de Sonido')
    ]
    path = models.CharField(max_length=100, choices=PATH_CHOICES, blank=True, null=True)

    CATEGORY_CHOICES = [
        ('onlyMusic', 'Musico solista'),
        ('onlyEquipment', 'Solo equipo tecnico y logistico'),
        ('complete', 'Ambiente Completa'),
        ('complementary', 'Compra complementaria')
    ]
    category = models.CharField(max_length=100, choices=PATH_CHOICES, blank=True, null=True)

    SOUND_SETUP_CHOICES = [
        ('own_equipment', 'Equipo propio'),
        ('musician_provided_equipment', 'Profesional lleva su propio equipo'),
        ('advice_needed', 'Requerimos asesoría'),
    ]
    sound_setup = models.CharField(max_length=50, choices=SOUND_SETUP_CHOICES, blank=True, null=True)

    CAPACITY_CHOICES = [
        ('Less_than_50', 'Menos de 50'),
        ('50_and_100', 'Entre 50 y 100'),
        ('100_and_300', 'Entre 100 y 300'),
        ('300_and_500', 'Entre 300 y 500'),
        ('more_than_500', 'Más de 500'),
    ]
    estimated_capacity = models.CharField(max_length=20, choices=CAPACITY_CHOICES, blank=True, null=True)

    # For more than 500 on capacity
    visit = models.ForeignKey(EventVisit, blank=True, null=True , on_delete=models.SET_NULL)

    # Sound restrictions
    sound_restriction = models.BooleanField(default=False)

    # Sound package -> is blank when you don't need this one
    sound_package = models.ForeignKey(SoundPackage, blank=True, null=True, on_delete=models.SET_NULL)

    # Event date and additional info
    event_date = models.DateField()

    DURATION_CHOICES = [
        ('one_hour', 'Menos de una hora'),
        ('one_and_two_hours', '1 - 2 horas'),
        ('three_and_four_hours', '3 - 4 horas'),
        ('custom', 'Más de 4 horas'),
    ]
    event_duration = models.CharField(max_length=20, choices=DURATION_CHOICES)

    # More than 4 hours option
    custom_duration = models.PositiveIntegerField(blank=True, null=True)  # just if is more than 4 hours

    referral_source = models.ForeignKey(ReferralSource, on_delete=models.SET_NULL, null=True, blank=True)

    additional_comments = models.TextField(blank=True, null=True)

    # User profile
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')

    # lista de artistas
    list_musicprojects = models.ManyToManyField(MusicProject, blank=True, related_name="orders")

    #lista de categorias
    categories_music = models.ManyToManyField(CategoryMusic, blank=True)

    #lista de equipment
    list_equipment = models.ManyToManyField(Equipment, blank=True)

    ideas_requirements = models.TextField(blank=True, null=True)

    # Budget
    min_budget = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Generate number order """
        if not self.order_number:
            today = now().strftime("%Y%m%d")
            last_order = Order.objects.filter(order_number__startswith=f"ORD-{today}").order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1]) + 1
            else:
                last_number = 1
            self.order_number = f"ORD-{today}-{last_number:05d}"  # Format ORD-YYYYMMDD-00001

        if not self.status:
            self.status = "CONCEPT_DEFINED"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    specific_service = models.ForeignKey(SpecificService, on_delete=models.SET_NULL, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    instruments = models.ManyToManyField(Instrument, blank=True)
    musician_voice_type = models.ForeignKey(MusicianVoiceType, on_delete=models.SET_NULL, null=True, blank=True)
    vocal_style = models.ForeignKey(VocalStyle, on_delete=models.SET_NULL, null=True, blank=True)
    dj_type = models.ForeignKey(DJType, on_delete=models.SET_NULL, null=True, blank=True)
    category_music = models.ForeignKey(CategoryMusic, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.specific_service}"


class AdditionalEquipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    equipment = models.ForeignKey("core.Equipment", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'equipment')  # Evita duplicados

    def __str__(self):
        return f"Order {self.order.id} - {self.equipment.name}"

